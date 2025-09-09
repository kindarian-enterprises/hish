# 🏗️ **Architectural & Code Design Principles**

## 🎯 **Purpose**
Foundational design principles that ensure code quality, maintainability, and cross-project consistency within the Hish framework ecosystem.

---

## 📐 **Architectural Principles**

### **Service Boundaries & Separation of Concerns**
- **Service Isolation**: Use gateways/transport abstractions, not direct service calls
- **Clean Architecture**: Separate business logic from infrastructure concerns
- **Domain-Driven Design**: Organize code around business domains, not technical layers
- **Interface Segregation**: Create focused, specific interfaces rather than monolithic ones

### **Configuration & Environment Management**
- **Configuration-Driven**: Use environment variables, not hardcoded values
- **Environment Parity**: Ensure development, staging, and production consistency
- **Secrets Management**: Never commit sensitive data, use proper secret management
- **Feature Flags**: Enable/disable features through configuration, not code changes

### **Error Handling & Resilience**
- **Centralized Error Handling**: Use consistent error handling patterns across services
- **Circuit Breaker Logic**: Prevent cascading failures with proper retry/fallback logic
- **Graceful Degradation**: Services should degrade functionality, not fail completely
- **Proper Exception Chaining**: Maintain error context through the call stack

### **Container-Native Development**
- **Containerized Consistency**: Develop and test in containers for environment parity
- **Docker Layer Optimization**: Separate stable dependencies from changing application code
- **Multi-Stage Builds**: Use different stages for building, testing, and production
- **Health Checks**: Implement proper container health checks for orchestration

---

## 🔧 **SOLID Principles Implementation**

### **Single Responsibility Principle (SRP)**
```python
# ✅ CORRECT: Each class has one reason to change
class UserValidator:
    def validate_email(self, email: str) -> bool:
        return "@" in email and "." in email

    def validate_password(self, password: str) -> bool:
        return len(password) >= 8

class UserRepository:
    def save_user(self, user: User) -> User:
        return self.db.save(user)

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter_by(email=email).first()

# ❌ WRONG: Multiple responsibilities in one class
class UserManager:
    def validate_and_save_user(self, user_data: dict):
        # Validation logic + persistence logic = SRP violation
        pass
```

### **Open/Closed Principle (OCP)**
```python
# ✅ CORRECT: Open for extension, closed for modification
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> bool:
        pass

class EmailSender(NotificationSender):
    def send(self, message: str, recipient: str) -> bool:
        # Email implementation
        return True

class SMSSender(NotificationSender):
    def send(self, message: str, recipient: str) -> bool:
        # SMS implementation
        return True

# Adding new notification types doesn't require modifying existing code
```

### **Liskov Substitution Principle (LSP)**
```python
# ✅ CORRECT: Subtypes are substitutable for their base types
class Storage(ABC):
    @abstractmethod
    def store(self, data: bytes) -> str:
        """Returns storage identifier"""
        pass

class LocalStorage(Storage):
    def store(self, data: bytes) -> str:
        # Local file storage implementation
        return f"local://{file_path}"

class CloudStorage(Storage):
    def store(self, data: bytes) -> str:
        # Cloud storage implementation
        return f"cloud://{object_id}"

# Both implementations can be used interchangeably
```

### **Interface Segregation Principle (ISP)**
```python
# ✅ CORRECT: Focused, specific interfaces
class Readable(Protocol):
    def read(self) -> bytes:
        pass

class Writable(Protocol):
    def write(self, data: bytes) -> int:
        pass

class Closeable(Protocol):
    def close(self) -> None:
        pass

# Clients only depend on interfaces they actually use
class DataProcessor:
    def __init__(self, reader: Readable):
        self.reader = reader

    def process(self) -> ProcessedData:
        data = self.reader.read()
        return self.transform(data)

# ❌ WRONG: Monolithic interface
class FileOperations(Protocol):
    def read(self) -> bytes: pass
    def write(self, data: bytes) -> int: pass
    def delete(self) -> None: pass
    def compress(self) -> None: pass
    def encrypt(self) -> None: pass
    # Forces all clients to depend on operations they don't use
```

### **Dependency Inversion Principle (DIP)**
```python
# ✅ CORRECT: Depend on abstractions, not concretions
class OrderService:
    def __init__(self,
                 payment_processor: PaymentProcessor,  # Abstract interface
                 inventory_service: InventoryService,   # Abstract interface
                 notification_service: NotificationService):  # Abstract interface
        self.payment = payment_processor
        self.inventory = inventory_service
        self.notifications = notification_service

    def process_order(self, order: Order) -> OrderResult:
        # High-level logic that doesn't depend on specific implementations
        if self.inventory.check_availability(order.items):
            result = self.payment.process_payment(order.total)
            if result.success:
                self.notifications.send_confirmation(order.customer)
                return OrderResult.success()
        return OrderResult.failure("Processing failed")

# ❌ WRONG: Direct dependency on concrete classes
class OrderService:
    def __init__(self):
        self.stripe_processor = StripePaymentProcessor()  # Concrete dependency
        self.postgres_inventory = PostgresInventoryService()  # Concrete dependency
        # Hard to test, hard to change implementations
```

---

## 🧪 **Testing Architecture Principles**

### **Test Pyramid Structure**
- **Unit Tests (70%)**: Fast, isolated, focused on single components
- **Integration Tests (20%)**: Test component interactions with real services
- **End-to-End Tests (10%)**: Full system validation with external dependencies

### **Test Organization**
```python
# Directory structure
tests/
├── unit/          # All mocked, fast execution
│   ├── services/
│   ├── models/
│   └── utils/
├── integration/   # Real services, comprehensive scenarios
│   ├── api/
│   ├── database/
│   └── external/
└── e2e/          # Full system tests
    └── workflows/
```

### **Test Quality Standards**
- **>90% test coverage** with meaningful assertions
- **Constants for test values**: `EXPECTED_CALL_COUNT = 2`, `HTTP_STATUS_CONFLICT = 409`
- **Proper test isolation**: Each test can run independently
- **Clear test naming**: `test_should_return_error_when_user_not_found`

---

## 📊 **Code Quality Standards**

### **Type Safety Requirements**
```python
# ✅ ALWAYS use modern type hints
def process_data(input: str | bytes | None) -> TaskResult:
    """Process input data with proper error handling."""

# ✅ ALWAYS define constants for magic numbers
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
HTTP_STATUS_CONFLICT = 409

# ✅ ALWAYS use proper exception chaining
try:
    risky_operation()
except OriginalError as err:
    raise CustomError("Context-specific message") from err
```

### **Performance & Observability**
- **Structured Logging**: Use consistent log formats with context
- **Health Checks**: Implement readiness and liveness probes
- **Metrics Collection**: Track key performance indicators
- **Tracing Hooks**: Enable distributed tracing for complex workflows

### **Security By Design**
- **Input Validation**: Validate all external inputs at boundaries
- **Authentication/Authorization**: Centralized identity and access management
- **Secrets Management**: Proper secret rotation and access control
- **Audit Logging**: Track security-relevant operations

---

## 🔄 **Continuous Improvement Principles**

### **Technical Debt Management**
- **Fix While Editing**: When touching any file, immediately fix linting/formatting issues
- **Refactor Incrementally**: Improve code structure during feature development
- **Document Decisions**: Record architectural decisions with rationale
- **Monitor Code Health**: Use automated tools to track code quality metrics

### **Knowledge Sharing**
- **Pattern Documentation**: Store successful solutions for ecosystem reuse
- **Anti-Pattern Learning**: Document failures to prevent repetition
- **Cross-Project Validation**: Validate patterns across multiple contexts
- **Continuous Learning**: Update principles based on real-world outcomes

---

**These principles create a foundation for scalable, maintainable, and reliable software systems that can evolve with changing requirements while maintaining high quality standards.**
