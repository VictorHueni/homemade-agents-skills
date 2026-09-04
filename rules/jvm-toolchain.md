# JVM toolchain preferences

Stated preferences (2026-09-01, while bootstrapping a greenfield JVM service):

- **Maven over Gradle** — "I'm more a Maven guy than a Gradle guy." Default new JVM projects to Maven multi-module; only use Gradle when a repo already standardises on it.
- **OpenJDK builds only, never the Oracle-licensed JDK** — pin Eclipse Temurin in CI and toolchain declarations; local Debian/distro OpenJDK is fine for dev.
- **Prefer the current LTS, not the previous one** — when I defaulted to the older LTS (21) as the "safe" choice, the owner pushed to the newer LTS (25); verify the framework/toolchain actually builds on it rather than assuming, then adopt it.

**How to apply:** greenfield JVM scaffolding = Maven wrapper committed (`only-script` distribution type is fine), `maven.compiler.release` on the current LTS, Temurin pinned in `mise.toml`/CI (`actions/setup-java` with `distribution: temurin`). On this machine, `mvn` on PATH resolves to a Windows-side Maven via WSL interop (`/mnt/c/Maven/...`) — never use it from WSL; use the project's `mvnw` or a Linux Maven.
