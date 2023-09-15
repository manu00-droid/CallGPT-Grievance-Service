package com.callgpt.database.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Complaint {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long cid;
    @ManyToOne
    @JoinColumn(name = "uid")
    private User user;
    private String description;
    private String department;

    public Complaint(User user, String complaintDescription, String department) {
        this.setUser(user);
        this.setDescription(complaintDescription);
        this.setDepartment(department);
    }
}