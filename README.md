# 🚀 AWS Serverless Data Processing Pipeline: S3, Lambda, SNS & CloudWatch Monitoring  

## 🛠 Overview  
This project automates the processing of **DoorDash delivery data** using **AWS Lambda, S3, SNS, and CodeBuild**. The workflow ensures efficient data processing and notifications for success/failure cases.  
**Note:**  This mini project was part of an assignment given in this course "AWS Services For Data Engineering" on grow data skills. While this project uses DoorDash-style delivery data, it is purely for learning purposes and is not affiliated with DoorDash.


## ⚙️ Architecture Diagram  
![s3_lambda_sns drawio](https://github.com/user-attachments/assets/31a8b6d6-2634-4eb6-b9ac-1efa7a14716b)
**Note:** AWS service icons used in this diagram are sourced from the official [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/) and were designed using Draw.io

---

## 🔥 **Workflow**  

### 1️⃣ **Setup S3 Buckets**
- Create two folders:
  - `doordash-landing-zn` (for raw JSON files)
  - `doordash-target-zn` (for processed files)  
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/d118e597-41e1-4e87-b28b-d8c13433932e)


---

### 2️⃣ **Set Up Amazon SNS Topic**
- Create an SNS topic for notifications & subscribe to an email to receive alerts.  
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/965b7a93-6058-4924-8331-6a7b3006701a)

![image](https://github.com/user-attachments/assets/d534535c-d41b-4456-8fa7-542994b511b3)


---

### 3️⃣ **Create & Configure AWS Lambda**
- Set up Lambda with a Python runtime.
- Grant permissions for **S3 & SNS**.  
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/c1a676f4-f954-41b7-bfab-27021f1db025)

![image](https://github.com/user-attachments/assets/d2e9624c-351f-418a-94f6-ce500a54e7ed)

  ---

- **Lambda Function Implementation:** The AWS Lambda function processes incoming JSON files and performs the following steps:

   ✅ Extract File Metadata: Reads file name, extracts the date, and verifies its format.
  
   ✅ Load & Process Data:

       - Reads JSON from S3 (Landing Zone) into a Pandas DataFrame.

       - Filters only delivered orders.

       - Converts the processed data back to JSON.
  
   ✅ Store Processed Data: Saves the filtered JSON to S3 (Processed Zone).
  
   ✅ Send Notifications via SNS:

       - Success Notification: Sent when file processing is completed.

       - Failure Notification: Sent if processing fails.
---

### 4️⃣ **End-to-End Testing: S3 Upload, Lambda Execution & SNS Notification**
- Upload a test file (`yyyy-mm-dd-raw_input.json`) to `doordash-landing-zn`.  
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/21ec683d-5177-4e05-a192-03165f8e4983)
 

- Lambda **filters** the data and saves it in `doordash-target-zn`.  
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/06d3c57a-f9e3-46b5-8552-345f81626436)


- **SNS sends a notification** upon processing.  
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/641639a7-0986-459a-b17e-a0819f033540)
 
Note: Using CloudWatch the logs can be monitored in case of failure.
---

### 5️⃣ **Set Up AWS CodeBuild for CI/CD**
- Connect **GitHub Repo** with CodeBuild.
- Add `lambda_function.py`, `requirements.txt`, and `buildspec.yml`.
- Use CloudWatch logs to verify build and deployment progress.
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/f1293288-0b9d-4572-8c99-5f6665edd99b)
 

- Push updates in GitHub → Start **CodeBuild** → Lambda updates automatically!  
📷 **Screenshot**  
![image](https://github.com/user-attachments/assets/08652e97-9a6b-4cf4-b146-e014c67ffe09)


---

