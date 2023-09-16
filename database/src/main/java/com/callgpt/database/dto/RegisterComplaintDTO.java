package com.callgpt.database.dto;

import lombok.Data;

@Data
public class RegisterComplaintDTO {
    private String name;
    private String aadhaarNumber;
    private String phoneNumber;
    private String state;
    private String city;
    private String language;
    private String complaintDescription;
    private String department;
}
