package com.callgpt.database.service;

import com.callgpt.database.entity.Complaint;
import com.callgpt.database.repository.ComplaintRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ComplaintService {
    private final ComplaintRepository complaintRepository;

    @Autowired
    public ComplaintService(ComplaintRepository complaintRepository) {
        this.complaintRepository = complaintRepository;
    }

    public Complaint save(Complaint complaint) {
        return complaintRepository.save(complaint);
    }
}
