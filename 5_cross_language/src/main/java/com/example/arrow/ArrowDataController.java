package com.example.arrow;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * REST Controller for Apache Arrow data analysis
 * Provides HTTP endpoints to analyze Arrow data
 */
@RestController
@RequestMapping("/api/arrow")
public class ArrowDataController {
    
    @Autowired
    private ArrowDataService arrowDataService;
    
    /**
     * Health check endpoint
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "UP");
        response.put("service", "Apache Arrow Consumer");
        response.put("framework", "Spring Boot");
        response.put("java_version", System.getProperty("java.version"));
        response.put("compiled_for", "Java 21 (runs on Java 25)");
        return ResponseEntity.ok(response);
    }
    
    /**
     * Analyze Arrow data file
     */
    @GetMapping("/analyze")
    public ResponseEntity<Map<String, Object>> analyze(
            @RequestParam(value = "filename", defaultValue = "shared_data.feather") String filename) {
        Map<String, Object> response = new HashMap<>();
        try {
            // Note: In a real application, you'd return structured data
            // For now, this triggers the analysis which prints to console
            arrowDataService.analyzeArrowData(filename);
            response.put("status", "success");
            response.put("message", "Analysis completed. Check console for results.");
            response.put("filename", filename);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", e.getMessage());
            return ResponseEntity.internalServerError().body(response);
        }
    }
}

