# FarmOps Flutter SaaS (Flutter 3.x)

Aplicativo profissional multi-plataforma (Android, iOS e Windows) para gestão financeira e operacional de fazendas, consumindo API FastAPI multi-tenant com RBAC.

## Stack
- Flutter 3.x / Dart 3
- Clean Architecture (domain/data/presentation)
- Riverpod
- Dio
- Hive (cache offline)
- flutter_secure_storage
- go_router
- fl_chart
- Material 3 + dark mode

## Estrutura
- `lib/core`: config, tema, rede, storage, erros, utilitários.
- `lib/features`: auth, farms, dashboard, finance (income/expense/categories), inventory, cattle, vaccinations, alerts, reports, settings.

## Pré-requisitos
- Flutter SDK 3.x
- Dart 3.x
- Android Studio / Xcode (macOS) / Visual Studio com Desktop development with C++ (Windows)

## Instalação
```bash
flutter pub get
```

## Configurar baseUrl (dev/prod)
O app lê por `--dart-define=BASE_URL`.

Exemplos:
```bash
flutter run -d windows --dart-define=BASE_URL=http://localhost:8000
flutter run -d android --dart-define=BASE_URL=http://10.0.2.2:8000
flutter run -d ios --dart-define=BASE_URL=http://localhost:8000
```

## Rodar Android
```bash
flutter run -d android --dart-define=BASE_URL=http://10.0.2.2:8000
```

## Rodar iOS
```bash
flutter run -d ios --dart-define=BASE_URL=http://localhost:8000
```

## Rodar Windows
```bash
flutter config --enable-windows-desktop
flutter run -d windows --dart-define=BASE_URL=http://localhost:8000
```

## Build APK release
```bash
flutter build apk --release --dart-define=BASE_URL=https://api.seu-dominio.com
```

## Build Windows release
```bash
flutter build windows --release --dart-define=BASE_URL=https://api.seu-dominio.com
```

## API local e remota
- Local: `http://localhost:8000` (Windows/iOS) ou `http://10.0.2.2:8000` (Android emulador).
- Remota: `https://api.seu-dominio.com`.

## Recursos implementados
- Login JWT (access + refresh) com persistência segura.
- Multi-fazenda com seleção de fazenda ativa e envio automático de `X-Farm-Id`.
- Dashboard com KPIs, margens, gráficos e alertas recentes.
- Financeiro: listar/criar receitas e despesas.
- Estoque: status e alertas visuais.
- Vacinação: lista e criação de registro.
- Alertas: listar e resolver (conforme RBAC).
- Export CSV Power BI.
- Cache offline com fallback automático via Hive.
- Layout adaptativo (sidebar desktop, navegação mobile).

