package com.example.arrow;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.CommandLineRunner;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Spring Boot Application for Apache Arrow Cross-Language Data Consumer
 * 
 * This application demonstrates reading and analyzing Arrow data created by Python
 * in a Spring Boot environment with Java 21+.
 * 
 * Note: Compiled with Java 21 for Spring Boot compatibility, but works with Java 25 runtime.
 * 
 * Usage:
 *   mvn spring-boot:run
 *   or
 *   mvn clean package && java -jar target/apache-arrow-java-consumer-1.0.0.jar
 */
@SpringBootApplication
public class ArrowConsumerApplication {

    public static void main(String[] args) {
        SpringApplication.run(ArrowConsumerApplication.class, args);
    }

    @Component
    static class ArrowDataRunner implements CommandLineRunner {
        
        @Autowired
        private ArrowDataService arrowDataService;
        
        @Override
        public void run(String... args) {
            System.out.println("============================================================");
            System.out.println("SPRING BOOT APACHE ARROW CONSUMER");
            System.out.println("============================================================");
            
            try {
                // Analyze the Arrow data
                arrowDataService.analyzeArrowData("shared_data.feather");
            } catch (Exception e) {
                System.err.println("Error analyzing Arrow data: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }
}

