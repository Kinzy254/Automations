function sendEmailsWithAttachments() {

  var startTime = new Date();

  var ss = SpreadsheetApp.openById("1AP2oEfEy6uxbRfJuUqY1-JX6FA61uG2UgcM1cj7Htx4");
  var sheet = ss.getSheets()[0]; // first tab
  var data = sheet.getDataRange().getValues();
  
  //Retrive resume from drive
  var resumeId = "1ScE5RCyQ-1dGBAOJXAhEyfZQA_z-AWse";
  var resume = DriveApp.getFileById(resumeId);

  var count = 0;
  for (var i = 1; i <= data.length; i++) { // <data.length
    count += 1;
    var email = data[i][3]; // Assuming email is in the correct column
    var firstName = (data[i][0]); // Assuming first name is in the correct column
    var documentId = (data[i][5]).split("/")[5]; // Assuming Document ID is in the correct column
    var status = data[i][6];
    if (status === "Sent" || firstName === "") {
      Logger.log('Skipping... ' +  firstName);
      continue;
    }
    Logger.log("No.>>> " + count);

    //Logger.log('Document ID: ' + documentId); // Check if the document ID is valid
    
    var subject = "APPLICATION FOR AN INTERNSHIP/ ENTRY-LEVEL POSITION IN AUDIT - LAETICIA IMBALA";
    var body = "Dear Hiring Manager,\n\nI hope this finds you well.\nI am writing to express my interest in joining your firm as an intern/entry-level audit associate. I hold a degree in Economics and Finance and I am eager to apply my analytical skills and financial knowledge within a professional audit environment. \nI am excited about this opportunity and I believe I can contribute effectively to your team's goals. \nAttached are my application letter and CV detailing my qualifications and experiences.\n\nI am eager to gain practical experience and knowledge from " + firstName + ". I look forward to hearing from you. \n\nWarm Regards, \nLaeticia Imbala \n0792972138 \nlaetimbala03@gmail.com.";

    try {
      // Get the file by ID
      var file = DriveApp.getFileById(documentId);
      Logger.log('File retrieved: ' + file.getName());
      Logger.log('File retrieved: ' + resume.getName());
      
      // Send the email with attachment
      MailApp.sendEmail({
        to: email,
        subject: subject,
        body: body,
        attachments: [file.getAs(MimeType.PDF), resume.getAs(MimeType.PDF)] // Change MimeType if necessary
      });
      sheet.getRange(i + 1, 7).setValue("Sent");
      var sleepTime = Math.floor(Math.random() * (5000 - 2000 + 1)) + 2000;
      Logger.log('Email sent\nSleeping abit... ' + sleepTime + ' ms');
      Utilities.sleep(sleepTime);
    } 
    catch (e) {
      if (e.message.includes("Service invoked too many times")) {
        Logger.log("Daily limit reached. Stopping script.");
        return;  // stop the function to avoid hard stop
      }
      Logger.log('Error sending email: ' + e.message);
      // Skip to the next iteration if there's an error
      continue;
    }
  }
  var endTime = new Date();
  var executionTime = (endTime - startTime) / 1000;
  Logger.log("\nExecution time: " + executionTime + " seconds");
}

