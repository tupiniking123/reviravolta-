# FarmOps Flutter (versão simplificada)

App Flutter 3.x para consumir a API FastAPI da fazenda.

## O que foi simplificado
- Layout mais simples (sidebar no desktop e navegação básica no mobile).
- Fluxo mais direto: login -> seleção de fazenda -> telas principais.
- Menos complexidade visual, mantendo o core:
  - JWT + refresh
  - Header `X-Farm-Id`
  - cache offline com Hive
  - RBAC no app
  - export CSV

## Requisitos
- Flutter 3.x
- Dart 3

## Solução para problema de Flutter SDK (sem instalação global)
Se sua máquina/CI não tiver `flutter`, use os wrappers do projeto:

```bash
./tooling/flutterw --version
./tooling/flutterw pub get
./tooling/flutterw run -d windows --dart-define=BASE_URL=http://localhost:8000
```

Eles baixam automaticamente o SDK para `./.flutter-sdk` (Linux/macOS).

> Windows nativo: recomenda-se WSL2 para usar os scripts bash, ou instalar SDK oficial e rodar os mesmos comandos com `flutter`.

## Rodar rápido
```bash
./tooling/flutterw pub get
./tooling/flutterw run -d windows --dart-define=BASE_URL=http://localhost:8000
```

### Android
```bash
./tooling/flutterw run -d android --dart-define=BASE_URL=http://10.0.2.2:8000
```

### iOS
```bash
./tooling/flutterw run -d ios --dart-define=BASE_URL=http://localhost:8000
```

## Build release
### APK
```bash
./tooling/flutterw build apk --release --dart-define=BASE_URL=https://api.seu-dominio.com
```

### Windows
```bash
./tooling/flutterw build windows --release --dart-define=BASE_URL=https://api.seu-dominio.com
```

## Estrutura
- `lib/core`: config, rede, storage, tema
- `lib/features`: auth, farms, dashboard, finance, inventory, vaccinations, alerts, reports, settings

