/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package screeningForm;

import eu.schudt.javafx.controls.calendar.DatePicker;
//import org.thehecklers.dialogfx;;

import java.awt.HeadlessException;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Orientation;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollBar;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.Priority;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import patientInfo.PatientInfoPane;
import patientForm7.PatientForm7;
import static patientForm7.PatientForm7.patientNumber;
import jfx.messagebox.MessageBox;

/**
 *
 * @author ktk15
 */
public class ScreeningFormPane extends GridPane {
    //public Button submitButton = new Button("Submit Patient");

    public CheckBox cbi1 = new CheckBox();
    public CheckBox cbi2 = new CheckBox();
    public CheckBox cbi3 = new CheckBox();
    public CheckBox cbe1 = new CheckBox();
    public CheckBox cbe2 = new CheckBox();
    public CheckBox cbe3 = new CheckBox();
    public CheckBox cbe4 = new CheckBox();
    public CheckBox cbe5 = new CheckBox();
    public CheckBox cbe6 = new CheckBox();
    public CheckBox cbe7 = new CheckBox();
    public CheckBox cbe8 = new CheckBox();
    public CheckBox cbe9 = new CheckBox();
    public TextField TF1 = new TextField();
    public TextField TF2 = new TextField();
    public TextField TF3 = new TextField();
    public TextField TF4 = new TextField();
    public TextField TF5 = new TextField();
    public TextField TF6 = new TextField();
    public TextField TF7 = new TextField();
    public DatePicker TF8 = new DatePicker(Locale.ENGLISH);

    public TextField TF9 = new TextField();
    public static int flagP = 0;
    public static int flagP2 = 0;

    private final PatientForm7 patientForm7;

    public static boolean isNumeric(String str) {
        return str.matches("-?\\d+(\\.\\d+)?");  //match a number with optional '-' and decimal.
    }

    private void PatientEntry(String str, Stage primary) {

        MessageBox.show(primary,
                str, "Information", MessageBox.ICON_INFORMATION);
    }

    private void ErrorMsg(String str, Stage primary) {
        MessageBox.show(primary,
                str, "Error", MessageBox.ICON_ERROR);
        flagP = 1;
        flagP2 = 1;
    }

    private void CheckTextField(TextField TF1, TextField TF2, TextField TF3,
            TextField TF4, TextField TF5, TextField TF6, TextField TF7,
            DatePicker TF8, TextField TF9) {
        flagP2 = 0;
        try {
            // Check NHI number input is in correct format
            if (TF1.getText().isEmpty()) {
                String error = "Plese input NHI number as 3 letters 4 numbers";
                ErrorMsg(error, (Stage) getScene().getWindow());

            } else if (!(TF1.getText().length() == 7)) {
                String error = "Plese input NHI number as 3 letters 4 numbers";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }

            int flag = 0;
            String[] result = TF1.getText().split("");
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
            }
            // Check Sex input is in correct format
            if (TF2.getText().isEmpty() || !(TF2.getText().length() == 1)) {
                String error = "Please input Sex as type M or F ";
                ErrorMsg(error, (Stage) getScene().getWindow());
            } else if (!(TF2.getText().equalsIgnoreCase("f") ^ TF2.getText().equalsIgnoreCase("m"))) {
                String error = "Please input Sex as type M or F ";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }
            // Check Age is a number and in correct format
            if (TF3.getText().isEmpty() && TF3.getText().length() <= 3) {
                String error = "Please input number into Age";
                ErrorMsg(error, (Stage) getScene().getWindow());
            } else if (!isNumeric(TF3.getText())) {
                String error = "Please input number into Age";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }
            if (!isNumeric(TF4.getText())) {
                String error = "Please input Arterial Pressure in mmHg";
                ErrorMsg(error, (Stage) getScene().getWindow());

            }
            float TF4float = Float.parseFloat(TF4.getText());
            if (TF4float < 0) {
                String error = "Please input Arterial Pressure in mmHg";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }

            if (!isNumeric(TF5.getText())) {
                String error = "Please enter the percentage value for the Fraction of Inspired Oxygen";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }
            float TF5float = Float.parseFloat(TF5.getText());
            if (TF5float < 0 || TF5float > 100) {
                String error = "Please enter the percentage value for the Fraction of Inspired Oxygen";
                ErrorMsg(error, (Stage) getScene().getWindow());

            }
            if (!isNumeric(TF6.getText())) {
                String error = "Please enter the percentage value for Peripheral capillary oxygen saturation";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }
            float TF6float = Float.parseFloat(TF6.getText());
            if (TF6float < 0 || TF6float > 100) {
                String error = "Please enter the percentage value for Peripheral capillary oxygen saturation";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }
            if (TF7.getText().isEmpty()) {
                String error = "Please input Ethnicity";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }

            if (TF8.getSelectedDate() == null) {
                String error = "Please select date from the calendar";
                ErrorMsg(error, (Stage) getScene().getWindow());

            } else if (TF8.getSelectedDate().after(new Date())) {
                String error = "Invalid date. Please select appropriate date";
                ErrorMsg(error, (Stage) getScene().getWindow());
            }

            if (TF9.getText().isEmpty()) {
                String error = "Please input Clinical Diagnostic";
                ErrorMsg(error, (Stage) getScene().getWindow());

            }
            if (PatientForm7.patientNumber - 1 >= 1) {
                for (int i = 0; i < PatientForm7.patientNumber - 1; i++) {
                    if (PatientForm7.NHIbuffer.get(i).equals(TF1.getText().toUpperCase())) {
                        String error = "Patient is already in database";
                        ErrorMsg(error, (Stage) getScene().getWindow());
                    }

                }
            }
            //HeadlessException | NumberFormatException | ArrayIndexOutOfBoundsException e)
        } catch (HeadlessException | NumberFormatException | ArrayIndexOutOfBoundsException e) {
            System.err.println("HeadlessException|NumberFormatException|ArrayIndexOutOfBoundsException: " + e.getMessage());
            flagP = 1;
        } finally {
            if (flagP2 == 0 && flagP == 1) {
                flagP = 0;
            }
        }
    }

    private void PatientInputLabel(final GridPane grid, int labelSize,
            int fontsizeLabel, int textWidth) {
        Label Title = new Label("Patient Information Sheet");
        Title.setFont(Font.font("Calibri", FontWeight.BOLD, 30));
        grid.add(Title, 0, 1, 10, 8);

        // NHI number Input
        Label NHI = new Label("Patient NHI Number");
        NHI.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(NHI, 0, 11);

        // Sex Input
        Label sex = new Label("Sex");
        sex.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(sex, 0, 15);

        // Age Input
        Label age = new Label("Age");
        age.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(age, 0, 19);

        // Arterial Blood Pressure Input
        Label paO = new Label("PaO2");
        paO.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(paO, 0, 23);

        // FiO2
        Label fio = new Label("Fio2");
        fio.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(fio, 0, 27);

        // SPO2
        Label spo = new Label("SPO2");
        spo.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(spo, 11, 11);

        // Ethnicity
        Label Ethnicity = new Label("Ethnicity");
        Ethnicity.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(Ethnicity, 11, 15);

        // Trial Admission Date
        Label AdmissionDate = new Label("Trial Admission Date");
        AdmissionDate.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(AdmissionDate, 11, 19);

        // Clinical Diagnostic
        Label Diagnostic = new Label("Clinical Diagnostic");
        Diagnostic.setFont(Font.font("Calibri", FontWeight.BOLD, fontsizeLabel));
        grid.add(Diagnostic, 11, 23);

        Label inclusion = new Label("Inclusion Criteria");
        inclusion.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        grid.add(inclusion, 0, 30, 10, 2);
        Label exclusion = new Label("Exclusion Criteria");
        exclusion.setFont(Font.font("Calibri", FontWeight.BOLD, 20));
        grid.add(exclusion, 0, 36, 10, 2);
    }

    private void resetText() {

        TF1.clear();
        TF2.clear();
        TF3.clear();
        TF4.clear();
        TF5.clear();
        TF6.clear();
        TF7.clear();
        TF8.setSelectedDate(new Date());
        TF8.setSelectedDate(null);
        TF9.clear();
        TF1.setPromptText("Enter Patient NHI Number");
        TF2.setPromptText("Enter Sex here, M or F");
        TF3.setPromptText("Enter age here");
        TF4.setPromptText("Enter Pressure here (mmHg)");
        TF5.setPromptText("Enter % Value here");
        TF6.setPromptText("Enter SPO2 here");
        TF7.setPromptText("Enter Ethnicity here");
        TF8.setPromptText("Enter Trial Admission Date Here");
        TF9.setPromptText("Enter Clincial Diagnostic here");
        cbi1.setSelected(false);
        cbi2.setSelected(false);
        cbi3.setSelected(false);
        cbe1.setSelected(false);
        cbe2.setSelected(false);
        cbe3.setSelected(false);
        cbe4.setSelected(false);
        cbe5.setSelected(false);
        cbe6.setSelected(false);
        cbe7.setSelected(false);
        cbe8.setSelected(false);
        cbe9.setSelected(false);

    }

    public void Input(GridPane grid, int labelSize, int textWidth) {
        TF1.setPromptText("Enter Patient NHI Number");
        TF1.setMinHeight(labelSize);
        TF2.setPromptText("Enter Sex here, M or F");
        TF2.setMinHeight(labelSize);
        TF3.setPromptText("Enter age here");
        TF3.setMinHeight(labelSize);
        grid.add(TF1, 0, 12);
        grid.add(TF2, 0, 16);
        grid.add(TF3, 0, 20);
        TF4.setPromptText("Enter Pressure here (mmHg)");
        TF4.setMinHeight(labelSize);
        grid.add(TF4, 0, 24);
        TF5.setPromptText("Enter % Value here");
        TF5.setMinHeight(labelSize);
        grid.add(TF5, 0, 28);
        TF6.setPromptText("Enter SPO2 here");
        TF6.setMinHeight(labelSize);
        grid.add(TF6, 11, 12);
        TF7.setPromptText("Enter Ethnicity here");
        TF7.setMinHeight(labelSize);
        grid.add(TF7, 11, 16);

        TF8.setDateFormat(new SimpleDateFormat("dd/MM/yy"));
        TF8.getCalendarView().todayButtonTextProperty().set("Today");
        TF8.getCalendarView().setShowWeeks(false);
        TF8.setPromptText("Select Trial Admission Date Here");
        TF8.setMinHeight(labelSize);
        TF8.setMinWidth(250);
        grid.add(TF8, 11, 20);
        TF9.setPromptText("Enter Clincial Diagnostic here");
        TF9.setMinHeight(labelSize + 130);
        TF9.setMinWidth(labelSize + 150);
        grid.add(TF9, 11, 24, 5, 8);

        cbi1.setText("I1  Patients requiring invasive mechanical ventilation (MV) (Intubation or tracheotomy).");
        cbi1.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        grid.add(cbi1, 0, 32);
        cbi2.setText("I2  PF (oxygen partial pressure to fraction of inspired oxygen) ratio <300mmHg.");
        cbi2.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        grid.add(cbi2, 0, 33);
        cbi3.setText("I3  Arterial line in situ.");
        cbi3.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        grid.add(cbi3, 0, 34);
        cbe1.setText("E1  Patients who are likely to be discontinued from MV within 24 hours.");
        cbe1.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe2.setText("E2  Patients with age < 16");
        cbe2.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe3.setText("E3  Patients who have moderate or severe traumatic brain injury, and/or have significant weakness from any neurological disease");
        cbe3.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe4.setText("E4  Patients who have a high spinal cord injury with loss of motor function and/ or have significant weakness from any neurological disease.");
        cbe4.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe5.setText("E5  Patients who have a Barotrauma (pneumothorax, pneumomediastinum, subcutaneous emphysema or any intercostal catheter for the treatment of air leak).");
        cbe5.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe6.setText("E6   Patients who have significant weakness from any neurological disease.Patients who have asthma as the primary presenting condition or a history of significant chronic obstructive pulmonary disease.");
        cbe6.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe7.setText("E7  Patients who are moribund and/or not expected to survive for > 72 hours.");
        cbe7.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe8.setText("E8  Patients who have already received MV for > 48 hours (including time spent ventilated in a referring unit).");
        cbe8.setFont(Font.font("Calibri", FontWeight.BOLD, 15));
        cbe9.setText("E9   Lack of clinical equipoise by intensive care unit (ICU) medical staff managing the patient.");
        cbe9.setFont(Font.font("Calibri", FontWeight.BOLD, 15));

        grid.add(cbe1, 0, 38, textWidth, 1);
        grid.add(cbe2, 0, 39, textWidth, 1);
        grid.add(cbe3, 0, 40, textWidth, 1);
        grid.add(cbe4, 0, 41, textWidth, 1);
        grid.add(cbe5, 0, 42, textWidth, 1);
        grid.add(cbe6, 0, 43, textWidth, 1);
        grid.add(cbe7, 0, 44, textWidth, 1);
        grid.add(cbe8, 0, 45, textWidth, 1);
        grid.add(cbe9, 0, 46, textWidth, 1);
    }

    public ScreeningFormPane(PatientForm7 patientForm) {

        
        
        //add(s1,0,1);
        //setHgrow(s1, Priority.ALWAYS);
        patientForm7 = patientForm;
        setAlignment(Pos.TOP_LEFT);
        setHgap(8);
        setVgap(8);
        setPadding(new Insets(25, 25, 25, 25));

        // Set font size;
        int fontsizeLabel = 16;
        int labelSize = 30;
        int textWidth = 20;
        //grid.setGridLinesVisible(true);
        PatientInputLabel(this, labelSize, fontsizeLabel, textWidth);

        Input(this, labelSize, textWidth);
        Button submitButton = new Button("Submit Patient");
        submitButton.setOnAction(new EventHandler<ActionEvent>() {

            public void handle(ActionEvent event) {
                // Check whether inputs are in correct format
                boolean InclusionCriteria = false;
                String protocol = "Excluded";
                CheckTextField(TF1, TF2, TF3, TF4, TF5, TF6, TF7, TF8, TF9);
                if (flagP == 0) {
                    Boolean pass = true;
                    //create new patient class and add the info to it.
                    patient p = new patient(patientNumber, TF1, TF2, TF3, TF4, TF5, TF6, TF7, TF8, TF9,
                            cbi1, cbi2, cbi3, cbe1, cbe2, cbe3, cbe4, cbe5, cbe6, cbe7, cbe8, cbe9);
                    boolean b1 = p.m_i1;
                    boolean b2 = p.m_i2;
                    boolean b3 = p.m_i3;
                    boolean b4 = p.m_e1;
                    boolean b5 = p.m_e2;
                    boolean b6 = p.m_e3;
                    boolean b7 = p.m_e4;
                    boolean b8 = p.m_e5;
                    boolean b9 = p.m_e6;
                    boolean b10 = p.m_e7;
                    boolean b11 = p.m_e8;
                    boolean b12 = p.m_e9;

                    if (p.m_age < 16) {
                        InclusionCriteria = false;
                        p.m_e2 = true;
                        b5 = true;
                    } else if ((p.m_age > 16) && p.m_e2 == true) {
                        p.m_e2 = false;
                        b5 = false;

                    }
                    if ((b4 == false) && (b5 == false) && (b6 == false) && (b7 == false)
                            && (b8 == false) && (b9 == false) && (b10 == false) && (b11 == false)
                            && (b12 == false) && (b1 == false) && (b2 == false) && (b3 == false)) {
                        ErrorMsg("Please select tick Box", (Stage) getScene().getWindow());

                        pass = false;
                    } else if ((b4 == true) || (b5 == true) || (b6 == true) || (b7 == true)
                            || (b8 == true) || (b9 == true) || (b10 == true)
                            || (b11 == true) || (b12 == true)) {

                        InclusionCriteria = false;
                    } else if ((b1 == true) && (b2 == true) && (b3 == true)) {
                        InclusionCriteria = true;
                    }
                    if ((InclusionCriteria == true) && (p.m_age < 16)) {
                        InclusionCriteria = false;
                        b5 = true;
                        p.m_e2 = true;

                    }

                    if (InclusionCriteria == false) {
                        protocol = "Excluded";

                    } else if (InclusionCriteria == true) {
                        protocol = "Included";
                    }
                    String str;
                    if (pass) {

                        try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(PatientForm7.directory, true)))) {

                            randomisationAlgorithm group = new randomisationAlgorithm(InclusionCriteria);

                            // Patient entry number and patient NHI number
                            out.printf("%d,", p.m_entry);
                            // Inclusion and exclusion criteria check box
                            out.printf(String.format("%s,%b,%b,%b,%b,%b,%b,%b,%b,%b,%b,%b,%b",
                                    p.m_nhi, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12));

                            out.printf(",%s,%d", p.m_sex, p.m_age); //sex ,age
                            out.printf(",%s,%s", p.m_height, p.m_weight); // Weight and Height not defined initially
                            out.printf(",%.3f,%.3f,%.3f", p.m_pao, p.m_fio, p.m_spo); //pao,fio,spo
                            out.printf(",%s,%s,%s", p.m_ethnicity, p.m_admissionDate, p.m_diagnostic); // eth/date/diag
                            out.printf(",%s,%s", p.m_protocol = protocol, p.m_group = group.m_groupString);
                            out.printf(",%s,%b,%s", p.m_apache, p.m_ards, p.m_ardsDate);

                            out.printf(",%s,%s,%s", p.m_famConsent, p.m_famDataConsent, p.m_patientConsent);
                            out.printf(",%s,%s", p.m_termdate, p.m_termreason);
                            out.printf(",%b,%s", p.m_mortality, p.m_mortalitydate);
                            out.printf(",%d", p.m_saenum);

                            for (int saeDate = 0; saeDate <= 29; saeDate++) {
                                out.printf(", ");

                            }

                            out.println();

                            out.close();

                            if (InclusionCriteria) {
                                str = "Thank You. Patient information has been received. Patient is included in: " + group.m_groupString;
                            } else {
                                str = "Thank You. Patient information has been received. Patient is excluded.";
                            }

                            PatientEntry(str, (Stage) getScene().getWindow());
                            resetText();

                        } catch (IOException e) {
                            System.err.println("IOException: " + e.getMessage());

                            //exception handling left as an exercise for the reader
                        }

                        // ADD the data to the table view table
                        patientForm7.patientInfoPane.table.getItems().add(
                                new PatientInfoPane.patient2(p));

                        patientNumber += 1;
                        PatientForm7.NHIbuffer.add(p.m_nhi);

                    }
                }

            }
        });
        submitButton.setMaxHeight(200);
        submitButton.setMaxWidth(300);
        add(submitButton, 18, 48);
        Button clearButton = new Button("Clear Entry");
        clearButton.setOnAction(new EventHandler<ActionEvent>() {

            public void handle(ActionEvent event) {
                resetText();
            }
        });
        add(clearButton, 18, 47);

    }

}
