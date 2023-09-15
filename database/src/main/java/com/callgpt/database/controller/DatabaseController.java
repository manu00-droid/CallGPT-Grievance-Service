package com.callgpt.database.controller;

import com.callgpt.database.dto.RegisterComplaintDTO;
import com.callgpt.database.entity.Complaint;
import com.callgpt.database.repository.ComplaintRepository;
import com.callgpt.database.repository.UserRepository;
import com.callgpt.database.entity.User;
import com.callgpt.database.service.ComplaintService;
import com.callgpt.database.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
public class DatabaseController {
    @Autowired
    private UserService userService;

    @Autowired
    private ComplaintService complaintService;

    @PostMapping("/register-complaint")
    public ResponseEntity<String> registerComplaint(@RequestBody RegisterComplaintDTO request) {
        String name = request.getName();
        String phoneNumber = request.getPhoneNumber();
        String aadhaarNumber = request.getAadhaarNumber();
        String city = request.getCity();
        String state = request.getState();
        String complaintDescription = request.getComplaintDescription();
        String department = request.getDepartment();
        try {
            Optional<User> userOptional = userService.getUserByPhoneNumber(phoneNumber);
            User user = userOptional.isPresent() ? userOptional.get() : new User(name, aadhaarNumber, phoneNumber, city, state);
            if (userOptional.isEmpty()) userService.save(user);
            Complaint complaint = new Complaint(user, complaintDescription, department);
            complaintService.save(complaint);
            //call msg service

            return ResponseEntity.ok("User and Complaint saved successfully.");
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error saving data.");
        }
    }

}
