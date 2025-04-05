# Step 1: Build the application using Maven
# Use a compatible Maven image with OpenJDK 17
FROM maven:3.8.4-openjdk-17 as build

# Set the working directory inside the container
WORKDIR /app

# Copy the pom.xml and download the dependencies
COPY pom.xml ./
RUN mvn dependency:go-offline

# Copy the entire project to the container
COPY src ./src

# Package the application to generate the JAR file
RUN mvn clean package -DskipTests

# Step 2: Create a new image with the JAR file
# Use a lightweight JDK image to run the application
FROM openjdk:17-jdk-slim


# Set the working directory
WORKDIR /app

# Copy the JAR file from the build stage
COPY --from=build /app/target/*.jar app.jar

# Expose the port the application runs on
EXPOSE 8080

# Command to run the application
ENTRYPOINT ["java", "-jar", "app.jar"]