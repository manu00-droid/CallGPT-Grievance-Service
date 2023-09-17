package com.callgpt.database.configuration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SmsServiceConfig {
    @Value("${sms.service.url}")
    private String smsServiceUrl;

    public String getSmsServiceUrl() {
        return smsServiceUrl;
    }
}
