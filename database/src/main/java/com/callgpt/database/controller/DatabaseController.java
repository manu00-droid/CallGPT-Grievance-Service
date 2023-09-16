package com.callgpt.database.controller;

import com.callgpt.database.dto.RegisterComplaintDTO;
import com.callgpt.database.entity.Complaint;
import com.callgpt.database.repository.ComplaintRepository;
import com.callgpt.database.repository.UserRepository;
import com.callgpt.database.entity.User;
import com.callgpt.database.service.ComplaintService;
import com.callgpt.database.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import javax.xml.crypto.Data;
import java.util.Optional;

@RestController
public class DatabaseController {
    private UserService userService;
    private ComplaintService complaintService;

    @Autowired
    public DatabaseController(UserService userService, ComplaintService complaintService) {
        this.userService = userService;
        this.complaintService = complaintService;
    }

    private static final String BASE_URI = "http://127.0.0.1:8083/translate/";
    private static WebClient webClient = WebClient.create(BASE_URI);

    @PostMapping("/register-complaint")
    public ResponseEntity<String> registerComplaint(@RequestBody RegisterComplaintDTO request) {
        String name = request.getName();
        String phoneNumber = request.getPhoneNumber();
        String aadhaarNumber = request.getAadhaarNumber();
        String city = request.getCity();
        String state = request.getState();
        String complaintDescription = request.getComplaintDescription();
        String department = request.getDepartment();
        String language = request.getLanguage();
        try {
            Optional<User> userOptional = userService.getUserByPhoneNumber(phoneNumber);
            User user = userOptional.isPresent() ? userOptional.get() : new User(name, aadhaarNumber, phoneNumber, city, state, language);
            if (userOptional.isEmpty()) userService.save(user);
            Complaint complaint = new Complaint(user, complaintDescription, department);
            complaint = complaintService.save(complaint);
            //call msg service
            DatabaseController.callSmsService(complaint, user);
            return ResponseEntity.ok("User and Complaint saved successfully.");
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error saving data.");
        }
    }

    private static void callSmsService(Complaint complaint, User user) {
        MultiValueMap<String, String> bodyValues = new LinkedMultiValueMap<>();
        bodyValues.add("cid", String.valueOf(complaint.getCid()));
        bodyValues.add("name", user.getName());
        bodyValues.add("phoneNumber", user.getPhoneNumber());
        bodyValues.add("department", complaint.getDepartment());
        bodyValues.add("complaintDescription", complaint.getDescription());
        bodyValues.add("language", user.getLanguage());

        webClient.post()
                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .body(BodyInserters.fromFormData(bodyValues))
                .retrieve()
                .toBodilessEntity()
                .subscribe(
                        responseEntity -> {
                            if (responseEntity.getStatusCode().is2xxSuccessful()) {
                                System.out.println("Sent SMS request success");
                            } else {
                                System.out.println("SMS request send fail");
                            }
                        },
                        error -> {
                            System.out.println(error.getMessage());
                        }
                );
    }
}

