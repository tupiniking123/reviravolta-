#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SDK_DIR="${ROOT_DIR}/.flutter-sdk"
CHANNEL="${FLUTTER_CHANNEL:-stable}"
VERSION="${FLUTTER_VERSION:-}"

OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

case "$OS" in
  linux) PLATFORM="linux" ;;
  darwin) PLATFORM="macos" ;;
  *)
    echo "SO não suportado por este script: $OS"
    echo "Use o Flutter SDK oficial para Windows ou configure WSL2."
    exit 1
    ;;
esac

case "$ARCH" in
  x86_64|amd64) ARCH_TAG="x64" ;;
  arm64|aarch64) ARCH_TAG="arm64" ;;
  *)
    echo "Arquitetura não suportada: $ARCH"
    exit 1
    ;;
esac

mkdir -p "$ROOT_DIR/.tool-cache"

if [ -x "$SDK_DIR/bin/flutter" ]; then
  echo "Flutter SDK já instalado em $SDK_DIR"
  exit 0
fi

if [ -n "$VERSION" ]; then
  ARCHIVE_NAME="flutter_${PLATFORM}_${ARCH_TAG}_${VERSION}-${CHANNEL}.tar.xz"
else
  ARCHIVE_NAME="flutter_${PLATFORM}_${ARCH_TAG}_${CHANNEL}.tar.xz"
fi

BASE_URL="https://storage.googleapis.com/flutter_infra_release/releases"
ARCHIVE_URL="${BASE_URL}/${CHANNEL}/${PLATFORM}/${ARCHIVE_NAME}"
ARCHIVE_PATH="${ROOT_DIR}/.tool-cache/flutter_sdk.tar.xz"

echo "Baixando Flutter SDK de: $ARCHIVE_URL"
if command -v curl >/dev/null 2>&1; then
  curl -fL "$ARCHIVE_URL" -o "$ARCHIVE_PATH"
elif command -v wget >/dev/null 2>&1; then
  wget -O "$ARCHIVE_PATH" "$ARCHIVE_URL"
else
  echo "É necessário curl ou wget para baixar o Flutter SDK."
  exit 1
fi

echo "Extraindo Flutter SDK..."
TMP_DIR="${ROOT_DIR}/.tool-cache/flutter-extract"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
tar -xJf "$ARCHIVE_PATH" -C "$TMP_DIR"

if [ ! -d "$TMP_DIR/flutter" ]; then
  echo "Falha ao extrair SDK (pasta flutter não encontrada)."
  exit 1
fi

rm -rf "$SDK_DIR"
mv "$TMP_DIR/flutter" "$SDK_DIR"

"$SDK_DIR/bin/flutter" --version

echo "OK: Flutter SDK instalado em $SDK_DIR"
