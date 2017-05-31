/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package addInfo;

import eu.schudt.javafx.controls.calendar.DatePicker;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.PasswordField;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleGroup;
import javafx.scene.layout.GridPane;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.stage.StageBuilder;
import javafx.stage.StageStyle;
import jfx.messagebox.MessageBox;
import patientInfo.PatientInfoPane;
import patientForm7.PatientForm7;

/**
 *
 * @author ktk15
 */
public class AddInfoPane extends GridPane {

    private final PatientForm7 patientForm7;
    public TextField ATF1 = new TextField();
    public TextField ATF2 = new TextField();
    public TextField ATF3 = new TextField();
    public TextField ATF4 = new TextField();
    private int patientNumberIndex = 0;
    //public TextField ATF5 = new TextField();
    DatePicker ATF5 = new DatePicker();
    DatePicker ATF7 = new DatePicker();
    DatePicker ATF8 = new DatePicker();
    DatePicker ATF9 = new DatePicker();
    public TextField ATF6 = new TextField();
    final ToggleGroup groupfam = new ToggleGroup();
    final ToggleGroup groupfamdata = new ToggleGroup();
    final ToggleGroup grouppat = new ToggleGroup();
    public RadioButton rb1 = new RadioButton();
    public RadioButton rb2 = new RadioButton();
    public RadioButton rb3 = new RadioButton();
    public RadioButton rb4 = new RadioButton();
    public RadioButton rb5 = new RadioButton();
    public RadioButton rb6 = new RadioButton();
    private final SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yy");
    private boolean loginBool;

    public AddInfoPane(PatientForm7 patientForm) {

        patientForm7 = patientForm;
        
        setAlignment(Pos.TOP_LEFT);
        setHgap(8);
        setVgap(8);
        setPadding(new Insets(25, 25, 25, 25));
        setup();
        Button clearButtn = new Button("Clear Fields");
        add(clearButtn, 30, 35);
        clearButtn.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                clearFields();
            }
        });
        Button Enter = new Button("Add Information");
        add(Enter, 60, 35);
        Enter.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                
                
                boolean pass = true;
                Date today = new Date();
                // first check for errors
                if (checkNHI() == true) {

                    if (!(ATF3.getText().isEmpty()) && checkWeightInput() == false) {
                        String error = "Plese input patient weight in numbers";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;

                    }
                    if ((!ATF2.getText().isEmpty()) && checkHeightInput() == false) {
                        String error = "Plese input patient height in numbers";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;
                    }
                    if ((!ATF4.getText().isEmpty()) && checkApacheInput() == false) {
                        String error = "Plese input patient apache code in numbers";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;
                    }
                    if (checkTermDate() == true && ATF5.getSelectedDate().after(today)) {
                        String error = "Selected date is in future";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;
                    }
                    if (checkTermDate() == true && ATF6.getText().isEmpty()) {
                        String error = "Please Enter termination reason!";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;
                    }
                    if (checkTermreason() == true && ATF5.getSelectedDate() == null) {
                        String error = "Please Enter termination date!";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;
                    }
                    if (checkMortalityDate() == true && ATF8.getSelectedDate().after(today)) {
                        String error = "Selected date is in future";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;
                    }
                    if (checkSAEDate() == true && ATF9.getSelectedDate().after(today)) {
                        String error = "Selected date is in future";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                        pass = false;
                    }
                    if (pass == true) {
                        login();
                        if (loginBool==true){
                        loadText();
                        clearFields();
                        patientForm7.patientInfoPane.data.clear(); // Removes all items
                        updateTable();
                        }
                    }
                }
            }
        });

    }
    
    protected final synchronized void updateTable() {
        ////////////////////////////
        try {

            File file = new File(PatientForm7.directory);
            file.getParentFile();
            BufferedReader text = new BufferedReader(new FileReader(file));
            String line;

            while ((line = text.readLine()) != null) {
                String[] result = line.split(",",67);
                PatientForm7.NHIbuffer.add(result[1]);
                //System.out.println(Arrays.toString(result));
                //System.out.println(result.length);
                int index = 0;
                patientForm7.patientInfoPane.data.add((new PatientInfoPane.patient2(result[index], result[index + 1], result[index + 2],
                        result[index + 3], result[index + 4], result[index + 5], result[index + 6],
                        result[index + 7], result[index + 8], result[index + 9], result[index + 10],
                        result[index + 11], result[index + 12], result[index + 13], result[index + 14],
                        result[index + 15], result[index + 16], result[index + 17], result[index + 18],
                        result[index + 19], result[index + 20], result[index + 21], result[index + 22],
                        result[index + 23], result[index + 24], result[index + 25], result[index + 26],
                        result[index + 27], result[index + 28], result[index + 29], result[index + 30],
                        result[index + 31], result[index + 32], result[index + 33], result[index + 34],
                        result[index + 35], result[index + 36], result[index + 37], result[index + 38],
                        result[index + 39], result[index + 40], result[index + 41], result[index + 42],
                        result[index + 43], result[index + 44], result[index + 45], result[index + 46],
                        result[index + 47], result[index + 48], result[index + 49], result[index + 50],
                        result[index + 51], result[index + 52], result[index + 53], result[index + 54],
                        result[index + 55], result[index + 56], result[index + 57], result[index + 58], 
                        result[index + 59], result[index + 60], result[index + 61], result[index + 62], 
                        result[index + 63], result[index + 64], result[index + 65], result[index + 66])));

                patientForm7.patientInfoPane.table.setItems(patientForm7.patientInfoPane.data);
            }
            text.close();

            //System.out.println(Arrays.toString(PatientForm6.NHIbuffer));
        } catch (IOException e) {
            System.err.println("IOException: " + e.getMessage());
        }
        /////////////////////////////////////////
    }
    
private void login() {

        GridPane grid = new GridPane();
        grid.setAlignment(Pos.CENTER);
        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(25, 25, 25, 25));
        Scene Scene2 = new Scene(grid, 300, 255);
        //Label userName = new Label("Please Enter password to add additional information");
        //grid.add(userName, 0, 1,30,1);


        Label pw = new Label("Password:");
        grid.add(pw, 0, 2);

        final PasswordField pwBox = new PasswordField();
        grid.add(pwBox, 1, 2);
        
        Button Enter = new Button("ENTER");
         grid.add(Enter, 1, 3);
         Button ExitBtn = new Button("Exit");
         grid.add(ExitBtn, 1, 4);
         
        final Stage stage = StageBuilder.create()
                .title("Login")
                .style(StageStyle.UTILITY)
                .resizable(false)
                .scene(Scene2)
                .build();
        
        ExitBtn.setOnAction(new EventHandler<ActionEvent>() {
                    
         @Override
         public void handle(ActionEvent e) {
             ((Node)(e.getSource())).getScene().getWindow().hide();
         }
        
         });
        
        Enter.setOnAction(new EventHandler<ActionEvent>() {
                    
         @Override
         public void handle(ActionEvent e) {
             
             if (pwBox.getText().endsWith("this is cure trial")){
                 loginBool = true;
                  MessageBox.show((Stage) getScene().getWindow(),
                "Thank you information has been added", "Information", MessageBox.ICON_INFORMATION);
              
             }
             else{
                 loginBool = false;
                 ErrorMsg("Invalid Password", (Stage) getScene().getWindow());
             }
             
             ((Node)(e.getSource())).getScene().getWindow().hide();
         }
        
         });

       stage.showAndWait();
    }


    protected final synchronized void loadText() {
        ////////////////////////////
        try (PrintWriter temptext = new PrintWriter(new BufferedWriter(new FileWriter(PatientForm7.tempdirectory, true)))) {

            File file = new File(PatientForm7.directory);
            file.getParentFile();
            BufferedReader text = new BufferedReader(new FileReader(file));

            String line;
            int counter = 0;
            while ((line = text.readLine()) != null) {
                boolean passDate = true;
                if (counter == patientNumberIndex) {
                    String[] result = line.split(",", 67);
                    Date admissionDate = formatter.parse(result[22]);
                    if (checkWeightInput() == true) {

                        result[17] = ATF3.getText();
                    }
                    if (checkHeightInput() == true) {
                        result[16] = ATF2.getText();
                    }
                    if (checkApacheInput() == true) {
                        result[26] = ATF4.getText();
                    }
                    if (checkArdsDate() == true) {
                        if ((ATF7.getSelectedDate().before(admissionDate))) {
                            passDate = false;
                            String error = "Error selected date is before patient admission date";
                            ErrorMsg(error, (Stage) getScene().getWindow());
                        } else {
                            result[28] = formatter.format(ATF7.getSelectedDate());
                            result[27] = "TRUE";
                        }
                    }
                    if (checkTermDate() == true) {
                        if ((ATF5.getSelectedDate().before(admissionDate))) {
                            passDate = false;
                            String error = "Error selected date is before patient admission date";
                            ErrorMsg(error, (Stage) getScene().getWindow());
                        } else {
                            result[32] = formatter.format(ATF5.getSelectedDate());
                        }
                    }
                    if (checkTermreason() == true) {
                        result[33] = ATF6.getText();
                    }
                    if (checkMortalityDate() == true) {
                        if ((ATF8.getSelectedDate().before(admissionDate))) {
                            passDate = false;
                            String error = "Error selected date is before patient admission date";
                            ErrorMsg(error, (Stage) getScene().getWindow());
                        } else {
                            result[34] = "TRUE";
                            result[35] = formatter.format(ATF8.getSelectedDate());
                        }
                    }
                    if (checkSAEDate() == true) {
                        if ((ATF9.getSelectedDate().before(admissionDate))) {
                            passDate = false;
                            String error = "Error selected date is before patient admission date";
                            ErrorMsg(error, (Stage) getScene().getWindow());
                        } else {

                            int saeNumber = Integer.parseInt(result[36]);
                            result[37 + saeNumber] = formatter.format(ATF9.getSelectedDate());
                            saeNumber++;

                            result[36] = String.valueOf(saeNumber);
                        }

                    }
                    if (rb1.isSelected()){
                        result[29] = "TRUE";
                        result[30] = "TRUE";
                    }
                    if (rb2.isSelected()){
                        result[29] = "FALSE";
                    }
                    if (rb3.isSelected()){
                        result[30] = "TRUE";
                    }
                    if (rb4.isSelected()){
                        result[30] = "FALSE";
                    }
                    if (rb5.isSelected()){
                        result[31] = "TRUE";
                    }
                    if (rb6.isSelected()){
                        result[31] = "FALSE";
                    }
                    if (passDate == true) {
                        String currentLine = Arrays.toString(result);

                        String regex = "\\[|\\]";
                        currentLine = currentLine.replaceAll(regex, "");
                        currentLine = currentLine.replaceAll(" ", "");

                        temptext.printf(currentLine);

                    } else {
                        temptext.print(line);
                    }
                } else {
                    temptext.print(line);
                }
                counter += 1;
                temptext.println();
            }
            text.close();
            temptext.close();
            File out = new File(PatientForm7.directory);

            out.delete();
            //patientInfo.PatientInfoPane.
            new File(PatientForm7.tempdirectory).renameTo(out);
        } catch (IOException | ParseException e) {
            System.err.println("IOException: " + e.getMessage());
        }

        /////////////////////////////////////////
    }

    public static boolean isNumeric(String str) {
        return str.matches("-?\\d+(\\.\\d+)?");  //match a number with optional '-' and decimal.
    }

    private Boolean checkSAEDate() {
        boolean passingVal = false;

        if (ATF9.getSelectedDate() != null) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkMortalityDate() {
        boolean passingVal = false;

        if (ATF8.getSelectedDate() != null) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkTermreason() {
        boolean passingVal = false;

        if ((!ATF6.getText().isEmpty())) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkTermDate() {
        boolean passingVal = false;

        if (ATF5.getSelectedDate() != null) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkArdsDate() {
        boolean passingVal = false;

        if (ATF7.getSelectedDate() != null) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkWeightInput() {
        boolean passingVal = false;

        if (isNumeric(ATF3.getText())) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkApacheInput() {
        boolean passingVal = false;

        if (isNumeric(ATF4.getText())) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkHeightInput() {
        boolean passingVal = false;

        if (isNumeric(ATF2.getText())) {
            passingVal = true;
        }
        return passingVal;
    }

    private Boolean checkNHI() {
        boolean pass = true;
        if (ATF1.getText().isEmpty()) {
            String error = "Plese input NHI number as 3 letters 4 numbers";
            ErrorMsg(error, (Stage) getScene().getWindow());
            pass = false;
        } else if (!(ATF1.getText().length() == 7)) {
            String error = "Plese input NHI number as 3 letters 4 numbers";
            ErrorMsg(error, (Stage) getScene().getWindow());
            pass = false;
        } else {

            int flag = 0;
            String[] result = ATF1.getText().split("");
            for (int i = 0; i <= 7; i++) {
                if (i <= 3) {
                    if (isNumeric(result[i])) {
                        flag = 1;

                    }
                } else if (i > 3 && i <= 7) {
                    if (!(isNumeric(result[i]))) {
                        flag = 1;
                    }
                }
            }

            if (flag == 1) {
                String error = "Plese input NHI number as 3 letters 4 numbers";
                ErrorMsg(error, (Stage) getScene().getWindow());
                pass = false;
            }
            if (PatientForm7.patientNumber <= 1) {
                String error = "Database is empty";
                ErrorMsg(error, (Stage) getScene().getWindow());
                pass = false;
            } else {
                boolean find = false;
                for (int i = 0; i < PatientForm7.patientNumber - 1; i++) {

                    if (PatientForm7.NHIbuffer.get(i).equals(ATF1.getText().toUpperCase())) {
                        patientNumberIndex = i;

                        find = true;

                    } else if (!(PatientForm7.NHIbuffer.get(i).equals(ATF1.getText().toUpperCase()))) {
                        if (find == false) {
                            find = false;
                        }
                    }

                }
                if (find == false) {
                    String error = "Patient is not in the database";
                    ErrorMsg(error, (Stage) getScene().getWindow());
                    pass = false;
                }
            }
        }
        return pass;
    }

    private void ErrorMsg(String str, Stage primary) {
        MessageBox.show(primary,
                str, "Error", MessageBox.ICON_ERROR);

    }

    private void clearFields() {
        ATF1.clear();
        ATF2.clear();
        ATF3.clear();
        ATF4.clear();
        ATF5.setSelectedDate(null);
        ATF6.clear();
        ATF7.setSelectedDate(null);
        ATF8.setSelectedDate(null);
        ATF9.setSelectedDate(null);
        ATF1.setPromptText("Enter Patient NHI Number");
        ATF4.setPromptText(("Enter patient's apache code"));
        ATF7.setPromptText(("Select date of which patient was diagnosed with ARDS"));
        ATF2.setPromptText(("Enter Patient's estimated height in m"));
        ATF5.setPromptText(("Select Patient termination Date"));
        ATF8.setPromptText(("Select Patient Mortality date"));
        ATF3.setPromptText(("Enter Patient's estimated Weight in kg"));
        ATF6.setPromptText(("Enter Patient termination reason"));
        ATF9.setPromptText(("Select Severe Advser Event date"));
        rb1.setSelected(false);
        rb2.setSelected(false);
        rb3.setSelected(false);
        rb4.setSelected(false);
        rb5.setSelected(false);
        rb6.setSelected(false);

    }

    private void setup() {
        setAlignment(Pos.TOP_LEFT);
        setHgap(10);
        setVgap(10);
        setPadding(new Insets(25, 25, 25, 25));
        Label Title = new Label("Additional Information");
        Title.setFont(Font.font("Calibri", FontWeight.BOLD, 30));
        add(Title, 3, 3, 40, 3);

        ////// FIRST COLUMN ///////
        Label NHInum = new Label("NHI Number");
        NHInum.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        ATF1.setPromptText("Enter Patient NHI Number");
        ATF1.setMinHeight(20);
        add(NHInum, 1, 10, 11, 2);
        add(ATF1, 1, 12, 11, 2);

        Label apache = new Label("Apache Code");
        apache.setFont(Font.font("Calibri", FontWeight.BOLD, 20));

        ATF4.setPromptText(("Enter patient's apache code"));
        ATF4.setMinHeight(20);
        add(ATF4, 1, 17, 11, 2);
        add(apache, 1, 15, 11, 2);

        Label ardsdate = new Label("ARDS diagnostic date");
        ardsdate.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        ATF7.setPromptText(("Select date of which patient was diagnosed with ARDS"));
        ATF7.setMinHeight(20);
        add(ardsdate, 1, 20, 11, 2);
        add(ATF7, 1, 22, 11, 2);

        Label famconsent = new Label("Family Consent");
        famconsent.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        add(famconsent, 1, 25, 11, 2);
        rb1.setText("Yes");
        rb2.setText("No");
        rb1.setToggleGroup(groupfam);
        rb2.setToggleGroup(groupfam);
        add(rb1, 1, 27);
        add(rb2, 1, 28);

        ////// Second COLUMN ///////
        Label height = new Label("Estiamted Height");
        height.setFont(Font.font("Calibri", FontWeight.BOLD, 20));

        ATF2.setPromptText(("Enter Patient's estimated height in m"));
        ATF2.setMinHeight(20);
        add(height, 25, 10, 11, 2);
        add(ATF2, 25, 12, 11, 2);

        Label termdate = new Label("Termination Date");
        termdate.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        add(termdate, 25, 15, 11, 2);
        ATF5.setPromptText(("Select Patient termination Date"));
        ATF5.setMinHeight(20);
        add(ATF5, 25, 17, 11, 2);

        Label mortalitydate = new Label("Mortality Date");
        mortalitydate.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        ATF8.setPromptText(("Select Patient Mortality date"));
        ATF8.setMinHeight(20);
        add(mortalitydate, 25, 20, 11, 2);
        add(ATF8, 25, 22, 11, 2);

        Label famdataconsent = new Label("Family Data Consent");
        famdataconsent.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        add(famdataconsent, 25, 25, 11, 2);
        rb3.setText("Yes");
        rb4.setText("No");
        rb3.setToggleGroup(groupfamdata);
        rb4.setToggleGroup(groupfamdata);
        add(rb3, 25, 27);
        add(rb4, 25, 28);

        ////// Third COLUMN ///////
        Label weight = new Label("Estiamted Weight");
        weight.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        ATF3.setPromptText(("Enter Patient's estimated Weight in kg"));
        ATF3.setMinHeight(20);

        add(weight, 50, 10, 11, 2);
        add(ATF3, 50, 12, 11, 2);

        Label termreason = new Label("Termination Reason");
        termreason.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        ATF6.setPromptText(("Enter Patient termination reason"));
        ATF6.setMinHeight(20);

        add(termreason, 50, 15, 11, 2);
        add(ATF6, 50, 17, 11, 2);

        Label saedate = new Label("SAE date");
        saedate.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        add(saedate, 50, 20, 11, 2);
        ATF9.setPromptText(("Select Severe Advser Event date"));
        ATF9.setMinHeight(20);
        add(ATF9, 50, 22, 11, 2);

        Label patconsent = new Label("Patient Consent");
        patconsent.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        add(patconsent, 50, 25, 11, 2);
        rb5.setText("Yes");
        rb6.setText("No");
        rb5.setToggleGroup(grouppat);
        rb6.setToggleGroup(grouppat);
        add(rb5, 50, 27);
        add(rb6, 50, 28);

    }
}
