/*
* If not stated otherwise in this file or this component's Licenses.txt file the
* following copyright and licenses apply:
*
* Copyright 2024 RDK Management
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*
http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package com.rdkm.tdkservice.controller;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Instant;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.rdkm.tdkservice.serviceimpl.AppUpgradeService;

/**
 * AppUpgradeController handles requests related to app upgrades
 */
@RestController
@CrossOrigin
@RequestMapping("/api/v1/app-upgrade")
public class AppUpGradeController {

    /**
     * AppUpgradeService bean for exporting device type changes to SQL.
     */
    @Autowired
    private AppUpgradeService appUpgradeService;

    /**
     * Exports change SQL based on the provided timestamp.
     * This endpoint triggers the SQL export process for app upgrades.
     * This change only SQL is used to get the changes added to the
     * database after a particular time stamp, it takes the changes
     * of device config and script related tables. Then these
     * SQL can be either integrated in the liquibase like tools or
     * directly applied to the existing database
     *
     * @param since - The time stamp from which the changes needs to be populated
     */
    @GetMapping("/exportChangeBasedOnTime")
    public ResponseEntity<byte[]> exportChangeSql(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) Instant since) {
        try {
            String filePath = "app_upgrade_changes_" + since.toString().replace(":", "-") + ".sql";
            appUpgradeService.writeAppUpgradeSqlToFile(since, filePath);
            Path path = Paths.get(filePath);
            byte[] fileBytes = Files.readAllBytes(path);
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.valueOf("application/sql"));
            headers.setContentDispositionFormData("attachment", filePath);
            return new ResponseEntity<>(fileBytes, headers, HttpStatus.OK);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(("Error exporting SQL: " + e.getMessage()).getBytes());
        }
    }
}
