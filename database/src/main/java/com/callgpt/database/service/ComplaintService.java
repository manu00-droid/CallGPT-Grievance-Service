package com.callgpt.database.service;

import com.callgpt.database.entity.Complaint;
import com.callgpt.database.repository.ComplaintRepository;
import com.callgpt.database.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ComplaintService {
    private final ComplaintRepository complaintRepository;

    @Autowired
    public ComplaintService(ComplaintRepository complaintRepository) {
        this.complaintRepository = complaintRepository;
    }

    public void save(Complaint complaint) {
        complaintRepository.save(complaint);
    }
}
