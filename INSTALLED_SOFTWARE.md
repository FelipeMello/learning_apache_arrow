# Installed Software Inventory

This document lists all software, libraries, and tools installed or referenced in this learning repository.

## System Information

- **OS**: Linux (based on user_info: linux 6.10.14-linuxkit)
- **Shell**: /bin/bash

## Programming Languages & Runtimes

### Python
- **Version**: 3.12 (May 2024)
- **Location**: `/usr/bin/python3` (assumed)
- **Package Manager**: pip3

### Node.js
- **Version**: 22 LTS (2024)
- **Package Manager**: npm
- **Location**: Installed system-wide

### Java
- **Version**: 25 (JDK 25) - September 2025
- **Runtime**: Java 25 (compiled for Java 21 for Spring Boot compatibility)
- **Build Tool**: Maven (optional, may need installation)

## Python Packages

### Core Data Processing
- **pyarrow**: >=22.0.0
  - Apache Arrow Python bindings
  - Used for: Columnar data processing, zero-copy operations

- **pandas**: >=2.3.3
  - Data analysis and manipulation library
  - Used for: DataFrame operations, data analysis

- **numpy**: >=2.3.4
  - Numerical computing library
  - Used for: Array operations, mathematical computations

### Python Standard Library (Built-in)
- datetime
- time
- os
- sys

## Node.js Packages

### Apache Arrow
- **apache-arrow**: ^16.1.0
  - Apache Arrow JavaScript/Node.js bindings
  - Used for: Cross-language data sharing, reading Arrow/Feather files

### Node.js Dependencies (via npm)
- Installed in: `/app/learning/learning_apache_arrow/cross_language/node_modules/`
- Note: `node_modules/` should be excluded from version control (in .gitignore)

## Java Libraries & Frameworks

### Apache Arrow Java
- **arrow-vector**: 16.0.0
  - Core Arrow vector implementation
- **arrow-memory-core**: 16.0.0
  - Memory management for Arrow
- **arrow-memory-netty**: 16.0.0
  - Netty-based memory allocator
- **arrow-format**: 16.0.0
  - Arrow format specification support

### Spring Boot
- **spring-boot-starter**: 3.4.0
  - Core Spring Boot starter
- **spring-boot-starter-web**: 3.4.0
  - Web application support (REST APIs)
- **spring-boot-configuration-processor**: 3.4.0
  - Configuration metadata processor
- **spring-boot-maven-plugin**: 3.4.0
  - Maven plugin for Spring Boot

### Build Tools
- **Maven**: (may need installation)
  - Used for: Java project build and dependency management
  - Installation: `apt-get install -y maven` (if not installed)

## Development Tools

### Version Control
- **Git**: 2.50+ (2025)
  - Version control system
  - Used for: Source code management

### Build Systems
- **Maven**: For Java projects
- **npm**: For Node.js projects
- **pip**: For Python projects

## Database Systems (Referenced)

### PostgreSQL
- **Version**: 16 (May 2024)
- **Status**: Referenced in agent system, may need installation
- **Client Tools**: psql (may need installation)

### Oracle Database
- **Version**: 19c (2019)
- **Status**: Referenced in agent system, prerequisites installed
- **Note**: Full installation requires manual setup

## Web Frameworks & Libraries

### React
- **Version**: 19.1.0 (March 2025)
- **Status**: Referenced in agent system
- **Usage**: Frontend development (not installed in this repo)

### Angular
- **Version**: 18 (2025)
- **Status**: Referenced in agent system
- **Usage**: Frontend development (not installed in this repo)

## File Formats & Data Formats

### Apache Arrow Formats
- **Arrow Format**: In-memory columnar format
- **Feather Format**: On-disk Arrow format
  - Used for: Cross-language data persistence
  - Compression: Uncompressed (for Node.js compatibility)

## System Utilities

### Shell & Scripting
- **Bash**: /bin/bash
- **Shell Scripts**: 
  - `run_all.sh` - Cross-language demonstration script
  - `regenerate_data.sh` - Data regeneration utility

### Text Processing
- Standard Unix utilities (grep, sed, awk, etc.)

## IDE & Editor Support

### Configuration Files
- `.gitignore` - Git ignore patterns
- `package.json` - Node.js project configuration
- `pom.xml` - Maven project configuration
- `requirements.txt` - Python dependencies

## Agent System (Custom)

### Python Agents
- **BaseAgent**: Base class for all agents
- **ReactUXAgent**: React & UX expert agent
- **JavaSpringBootAgent**: Java & SpringBoot expert agent
- **DatabasePerformanceAgent**: Database & performance expert agent
- **DevOpsSecurityAgent**: DevOps & security expert agent
- **AgentManager**: Agent coordination manager

## Installation Status

### ✅ Confirmed Installed
- Python 3.12
- Node.js 22 LTS
- Java 25 (JDK 25)
- Git 2.50+
- Python packages: pyarrow, pandas, numpy
- Node.js package: apache-arrow

### ⚠️ May Need Installation
- Maven (for Java builds)
- PostgreSQL client tools
- Additional system packages

### 📝 Referenced (Not Installed in Repo)
- React 19.1.0
- Angular 18
- PostgreSQL 16 (server)
- Oracle Database 19c (server)

## Package Management Commands

### Python
```bash
pip3 install -r requirements.txt
pip3 list  # List installed packages
```

### Node.js
```bash
cd learning/learning_apache_arrow/cross_language
npm install  # Install dependencies
npm list  # List installed packages
```

### Java/Maven
```bash
cd learning/learning_apache_arrow/cross_language
mvn dependency:tree  # List dependencies
mvn clean install  # Build project
```

## Notes

- This inventory is based on configuration files and documentation in the repository
- Some tools may need to be installed separately (e.g., Maven)
- Build artifacts (`target/`, `node_modules/`) are excluded from version control
- Generated data files (`.feather`, `.parquet`) are excluded from version control
- All Python packages should be installed with: `pip3 install -r requirements.txt --break-system-packages` (if needed)

## Last Updated

Generated based on repository state as of the current date.

