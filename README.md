# harness-cg-plugin

#Parameters
| Parameter                        |  Description                      |
| -------------------------------- | ---------------------------       |
| HARNESS_ACCOUNT_ID               | Account Id of Harness CG CD       |
| HARNESS_APPLICATION_ID           | Harness Application ID for CD     |
| HARNESS_API_KEY                  | Harness API Key under Users (CG)  |
| HARNESS_SERVICE                  | Service name to be deployed (CG)  |
| HARNESS_WEBHOOK_ID               | Pipeline trigger webhood ID (CG)  |
| HARNESS_BUILD_NUMBER             | Artifact Version            (CG)  |
| HARNESS_ARTIFACT_SOURCE_ENABLED  | Enable or Disable artifact source |
| HARNESS_ARTIFACT_SOURCE_NAME     | Artifact source name        (CG)  |
| HARNESS_PARAMETERS_ENABLED       | CD Parameters Enable or Disable   |
| HARNESS_PIPELINE_PARAMETERS      | CD Parameters JSON format         |



#Example yaml
````
```
                          - step:
                                type: Plugin
                                name: harness-deploy-cg
                                identifier: harnessdeploycg
                                spec:
                                    connectorRef: nikpdockerhub
                                    image: nikpap/harness-ci-cd-windows:latest
                                    privileged: true
                                    settings:
                                        HARNESS_ACCOUNT_ID: abcdefg1234
                                        HARNESS_APPLICATION_ID: abcdefg1234
                                        HARNESS_API_KEY: abcdefg1234=
                                        HARNESS_WEBHOOK_ID: abcdefg1234
                                        HARNESS_BUILD_NUMBER: latest
                                        HARNESS_SERVICE: my-service
                                        HARNESS_SERVICE_SOURCENAME: repo_image-name
                                        HARNESS_PARAMETERS_ENABLED: "TRUE"
                                        HARNESS_ARTIFACT_SOURCE_ENABLED: "TRUE"
                                        HARNESS_PARAMETERS: {"PARAM1":"TEST"}
                                    imagePullPolicy: IfNotPresent
                                when:
                                    stageStatus: Success
                                failureStrategies: []

```
````

