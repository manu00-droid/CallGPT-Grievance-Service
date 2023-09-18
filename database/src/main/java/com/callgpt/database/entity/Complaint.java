package com.callgpt.database.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

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
    @OnDelete(action = OnDeleteAction.CASCADE)
    private User user;
    private String description;
    private String department;
    private String status;

    @PrePersist
    public void prePersist() {
        if (getStatus() == null) {
            setStatus("in-progress");
        }
    }

    public Complaint(User user, String complaintDescription, String department) {
        this.setUser(user);
        this.setDescription(complaintDescription);
        this.setDepartment(department);
    }
}