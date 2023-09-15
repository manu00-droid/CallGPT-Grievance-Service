package com.callgpt.database.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor

public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long uid;
    private String name;
    @Column(unique = true, length = 12)
    private String aadhaarCard;
    private String city;
    private String state;
    @Column(nullable = false, unique = true, length = 10)
    private String phoneNumber;

}
