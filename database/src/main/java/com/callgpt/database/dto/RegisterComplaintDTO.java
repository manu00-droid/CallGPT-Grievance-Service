package com.callgpt.database.dto;

import lombok.Data;

@Data
public class RegisterComplaintDTO {
    private String client_name;
    private String aadhaar_card_number;
    private String phone_number;
    private String full_address;
    private String pincode;
    private String state;
    private String city;
    private String language;
    private String complaint_description;
    private String department;
}
