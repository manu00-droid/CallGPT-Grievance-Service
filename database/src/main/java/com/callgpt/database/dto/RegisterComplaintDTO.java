package com.callgpt.database.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
public class RegisterComplaintDTO {
    private String name;
    private String phoneNumber;
    private String state;
    private String city;
    private String aadhaarNumber;
    private String complaintDescription;
    private String department;
}
