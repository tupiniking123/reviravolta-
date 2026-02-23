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

## Rodar rápido
```bash
flutter pub get
flutter run -d windows --dart-define=BASE_URL=http://localhost:8000
```

### Android
```bash
flutter run -d android --dart-define=BASE_URL=http://10.0.2.2:8000
```

### iOS
```bash
flutter run -d ios --dart-define=BASE_URL=http://localhost:8000
```

## Build release
### APK
```bash
flutter build apk --release --dart-define=BASE_URL=https://api.seu-dominio.com
```

### Windows
```bash
flutter build windows --release --dart-define=BASE_URL=https://api.seu-dominio.com
```

## Estrutura
- `lib/core`: config, rede, storage, tema
- `lib/features`: auth, farms, dashboard, finance, inventory, vaccinations, alerts, reports, settings

