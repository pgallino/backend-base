# backend-base

Información sobre despliegue a AWS (ECR + App Runner) y CI con GitHub Actions
----------------------------------------------------------------------------

Este documento explica cómo desplegar la imagen Docker de este repo a Amazon ECR y servirla con AWS App Runner, así como la integración con GitHub Actions para automatizar builds y despliegues solo cuando los tests y checks pasen correctamente.

Resumen del flujo
- GitHub Actions (o tu máquina) construye la imagen Docker.
- La imagen se push a un repositorio ECR en la región donde esté App Runner (recomendado: `us-east-1`).
- App Runner (configurado en la misma región) obtiene la imagen del ECR y la ejecuta.
- Opcional: App Runner puede estar configurado con "Automatic deployments" para desplegar cada vez que llega una nueva imagen :latest, o puedes forzar un despliegue vía API desde el workflow.

1) Requisitos previos
- AWS account con método de pago activo (para evitar bloqueos de servicios).
- AWS CLI v2 instalado y configurado localmente (opcional para pruebas manuales).
- Docker instalado (para pruebas locales).
- GitHub repository con Secrets configurados (ver sección de Secrets).
- Región recomendada para App Runner: `us-east-1` (App Runner no está disponible en todas las regiones; asegurarse antes).

2) Crear repositorio ECR (región donde usarás App Runner)
Por consola:
- AWS Console → Elastic Container Registry → Create repository → nombre `backend-base`.
- Asegúrate de crear el repo en `us-east-1` (u otra región donde App Runner esté disponible).

Por CLI:
```bash
aws ecr create-repository --repository-name backend-base --region us-east-1
```

3) Construir, taggear y push desde tu máquina (comandos)
Reemplaza `AWS_ACCOUNT_ID` por tu número de cuenta (ej. `541064517549`) y asegúrate de estar en la región correcta.

```bash
# Loguear en ECR (us-east-1)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Construir
docker build -t backend-base .

# Taggear
docker tag backend-base:latest AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/backend-base:latest

# Subir
docker push AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/backend-base:latest
```

4) Crear servicio App Runner (consola)
- AWS Console → App Runner → Create service.
- Source type: Container registry → Amazon ECR.
  - Selecciona el repo `backend-base` en `us-east-1` y `latest`.
- Deployment settings:
  - Si querés despliegues automáticos marca “Enable automatic deployments”.
- Service settings:
  - Nombre del servicio: `backend-base-apprunner` (u otro).
  - CPU / Memory: usa la configuración mínima (ej. `0.25 vCPU / 0.5 GB`) para pruebas.
  - Puerto: `8000` (si tu app usa ese puerto).
- Access to image:
  - Opción recomendada: seleccioná "Create a new role" para que App Runner cree el role necesario que permita leer ECR.
- Observability: habilitá logs a CloudWatch para debugging.
- Create and deploy.

Nota: App Runner debe estar en la misma región que el repo ECR que contiene la imagen.

5) Crear IAM user para CI (GitHub Actions)
- Crea un IAM user con Programmatic access y añade permisos mínimos para ECR:
  - Managed policy recomendada: `AmazonEC2ContainerRegistryFullAccess`
  - (Opcional si el workflow fuerza despliegues en App Runner) añadir permiso `apprunner:StartDeployment` o la policy `AWSAppRunnerFullAccess` si corresponde.

Ejemplo de policy mínima para push a ECR (puedes usarla como base):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect":"Allow",
      "Action":["ecr:GetAuthorizationToken"],
      "Resource":"*"
    },
    {
      "Effect":"Allow",
      "Action":[
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:GetDownloadUrlForLayer",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:PutImage",
        "ecr:CreateRepository",
        "ecr:DescribeRepositories",
        "ecr:ListImages"
      ],
      "Resource":"*"
    }
  ]
}
```

6) Añadir GitHub Secrets
En el repo GitHub → Settings → Secrets and variables → Actions:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_ACCOUNT_ID
- (Opcional) APP_RUNNER_SERVICE_ARN — si quieres que el workflow fuerce un despliegue en App Runner con la API `start-deployment`.

7) Automatizar con GitHub Actions (dos opciones)
- Opción A: añadir el job de deploy en el mismo workflow de tests con `needs: check-quality`.
- Opción B (recomendada): workflow separado que se ejecuta solo cuando el workflow de tests termina con éxito (`workflow_run`), manteniendo responsabilidad separada.

Ejemplo de workflow independiente (.github/workflows/deploy-ecr.yml) que solo se ejecuta después de que el workflow "Code Quality Checks - Tests" termine con éxito:

```yaml
name: Build and push Docker image to ECR (triggered after tests)

on:
  workflow_run:
    workflows:
      - "Code Quality Checks - Tests"
    types:
      - completed

jobs:
  deploy-after-tests:
    if: ${{ github.event.workflow_run.conclusion == 'success' && github.event.workflow_run.head_branch == 'main' }}
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Ensure ECR repository exists
        run: |
          aws ecr describe-repositories --repository-names "backend-base" --region "us-east-1" || \
            aws ecr create-repository --repository-name "backend-base" --region "us-east-1"

      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1

      - name: Set up QEMU and Docker Buildx
        uses: docker/setup-qemu-action@v2

      - name: Build and push image to ECR
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com/backend-base:latest
          platforms: linux/amd64

      - name: Output image uri
        run: echo "Image pushed: ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com/backend-base:latest"

      # Opcional: forzar el despliegue en App Runner si NO usás Automatic Deployments
      - name: Trigger App Runner deployment (optional)
        if: ${{ secrets.APP_RUNNER_SERVICE_ARN != '' }}
        run: |
          aws apprunner start-deployment --service-arn "${{ secrets.APP_RUNNER_SERVICE_ARN }}" --region "us-east-1"
```

8) Pruebas locales antes de push
```bash
# Ejecutar localmente para comprobar arranque
docker run -e PORT=8000 -p 8000:8000 backend-base
# Abrir http://localhost:8000
```

9) Control de costes y limpieza
- App Runner cobra por capacidad mientras el servicio esté activo. Para evitar cargos:
  - Eliminar servicio App Runner cuando no lo uses: App Runner → Service → Delete service.
  - Borrar imágenes ECR que no necesites: ECR → repository → Delete images.
  - Crear un Budget en AWS Billing y configurar alertas:
    - AWS Console → Billing → Budgets → Create budget → Cost budget → configurar umbral y alertas.
- Para pausar pruebas, lo más rápido es eliminar el servicio App Runner y recrearlo cuando necesites.

10) Troubleshooting rápido
- Error: App Runner no encuentra la imagen → verificar que el repo ECR y App Runner estén en la misma región.
- Error: permisos → asegúrate que App Runner tenga un role que permita leer ECR (o deja que App Runner cree el role).
- Error en startup del contenedor → ver logs en App Runner → Logs (o CloudWatch si está habilitado).
- GitHub Actions falla con permisos → comprobar que el IAM user tenga permisos ECR y (si se usa) `apprunner:StartDeployment`.

11) Migración a OIDC (opcional, recomendado)
- En lugar de long‑lived AWS keys en GitHub Secrets, puedes configurar GitHub Actions OIDC trust con un role en AWS para obtener credenciales temporales. Esto mejora la seguridad. Si querés hago los pasos para configurarlo.

---

Si querés, agrego este texto al README del repo (puedo crear el patch/PR) o te doy el snippet listo para pegar. También puedo:
- Generar el archivo `.github/workflows/deploy-ecr.yml` y dejarlo listo para commitear,
- O modificar tu `main.yml` para añadir `needs: check-quality` y añadir el job de deploy en el mismo workflow.

Dime qué preferís que haga ahora y lo dejo listo.
```