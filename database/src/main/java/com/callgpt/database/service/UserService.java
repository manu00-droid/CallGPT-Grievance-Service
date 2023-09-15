package com.callgpt.database.service;

import com.callgpt.database.entity.User;
import com.callgpt.database.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {
    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public Optional<User> getUserByPhoneNumber(String phoneNumber) {
        return Optional.ofNullable(userRepository.findByPhoneNumber(phoneNumber));
    }

    public void save(User user) {
        userRepository.save(user);
    }
}
