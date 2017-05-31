/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package patientInfo;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableColumnBuilder;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.GridPane;
import patientForm7.PatientForm7;
/**
 *
 * @author ktk15
 */
public class PatientInfoPane extends GridPane{
    public TableView<patient2> table = new TableView<patient2>();
    public final ObservableList<patient2> data
            = FXCollections.observableArrayList();

    private PatientForm7 patientForm7;

    public PatientInfoPane(PatientForm7 patientForm) {

        patientForm7 = patientForm;

        setAlignment(Pos.TOP_LEFT);
        setHgap(8);
        setVgap(8);
        setPadding(new Insets(25, 25, 25, 25));
        /* 
         Creates main headings for the table view of patient entries
         */
        TableColumn patientIDC = TableColumnBuilder.create()
                .text("Patient ID")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn IC = TableColumnBuilder.create()
                .text("Inclusion Criteria")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn EC = TableColumnBuilder.create()
                .text("Exclusion Criteria")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn patientInfoC = TableColumnBuilder.create()
                .text("Patient Information")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn rctC = TableColumnBuilder.create()
                .text("RCT")
                .resizable(false)
                .editable(false)
                .build();

        TableColumn apacheC = TableColumnBuilder.create()
                .text("Apache")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn ardsC = TableColumnBuilder.create()
                .text("ARDS")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn consentC = TableColumnBuilder.create()
                .text("Trial Consent")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn terminationC = TableColumnBuilder.create()
                .text("Patient Termination")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn mortalC = TableColumnBuilder.create()
                .text("Mortality")
                .resizable(false)
                .editable(false)
                .build();
        TableColumn saeC = TableColumnBuilder.create()
                .text("Severe Adverse Events")
                .resizable(false)
                .editable(false)
                .build();

        table.getColumns().setAll(patientIDC, IC, EC, patientInfoC, rctC, apacheC, ardsC,
                consentC, terminationC, mortalC, saeC);
        // Patient Entry Number
        TableColumn tc1 = new TableColumn("Number");
        tc1.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("number"));
        tc1.setMinWidth(100);
        // Patient NHI Number
        TableColumn tc2 = new TableColumn("NHI Number");
        tc2.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("nhi"));
        tc2.setMinWidth(100);
        patientIDC.getColumns().addAll(tc1, tc2);

        // Inclusion Criteria
        for (int I = 1; I < 4; I++) {
            TableColumn tc = new TableColumn("IC" + I);
            IC.getColumns().addAll(tc);
            tc.setCellValueFactory(
                    new PropertyValueFactory<patient2, String>("ic" + I));
            tc.setMinWidth(100);
        }
        // Exclusion Criteria
        for (int J = 1; J < 10; J++) {
            TableColumn tc = new TableColumn("EC" + J);
            EC.getColumns().addAll(tc);
            tc.setCellValueFactory(
                    new PropertyValueFactory<patient2, String>("ec" + J));
            tc.setMinWidth(100);
        }

        // Info from Screening form
        TableColumn tc3 = new TableColumn("Sex");
        tc3.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("sex"));
        tc3.setMinWidth(100);

        TableColumn tc4 = new TableColumn("Age");
        tc4.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("age"));
        tc4.setMinWidth(100);

        TableColumn tc5 = new TableColumn("Estimated Height");
        tc5.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("height"));
        tc5.setMinWidth(200);

        TableColumn tc6 = new TableColumn("Estimated Weight");
        tc6.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("weight"));
        tc6.setMinWidth(200);

        TableColumn tc7 = new TableColumn("Pa02");
        tc7.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("pao"));
        tc7.setMinWidth(100);

        TableColumn tc8 = new TableColumn("Fi02");
        tc8.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("fio"));
        tc8.setMinWidth(100);

        TableColumn tc9 = new TableColumn("SP02");
        tc9.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("spo"));
        tc9.setMinWidth(100);

        TableColumn tc10 = new TableColumn("Ethnicity");
        tc10.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("ethnicity"));
        tc10.setMinWidth(100);

        TableColumn tc11 = new TableColumn("Admission Date");
        tc11.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("admission"));
        tc11.setMinWidth(100);
        TableColumn tc12 = new TableColumn("Clinical Diagnostic");
        tc12.setCellValueFactory(
                new PropertyValueFactory<patient2, String>("diagnostic"));
        tc12.setMinWidth(300);

        patientInfoC.getColumns().addAll(tc3, tc4, tc5, tc6, tc7, tc8, tc9, tc10, tc11, tc12);
        // RCT
        TableColumn tc13 = TableColumnBuilder.create()
                .text("Protocol")
                .minWidth(100)
                .cellValueFactory(new PropertyValueFactory("protocol"))
                .build();
        TableColumn tc14 = TableColumnBuilder.create()
                .text("Group Ascension")
                .minWidth(150)
                .cellValueFactory(new PropertyValueFactory("group"))
                .build();
        rctC.getColumns().setAll(tc13, tc14);
        // APACHE
        TableColumn tc15 = TableColumnBuilder.create()
                .text("APACHE III diagnostic code")
                .minWidth(200)
                .cellValueFactory(new PropertyValueFactory("apache"))
                .build();
        apacheC.getColumns().setAll(tc15);
        // Ards
        TableColumn tc21 = TableColumnBuilder.create()
                .text("ARDS")
                .minWidth(100)
                .cellValueFactory(new PropertyValueFactory("ards"))
                .build();
        TableColumn tc22 = TableColumnBuilder.create()
                .text("ARDS Date")
                .minWidth(100)
                .cellValueFactory(new PropertyValueFactory("ardsdate"))
                .build();
        ardsC.getColumns().setAll(tc21, tc22);
        // Consent
        TableColumn tc16 = TableColumnBuilder.create()
                .text("Family Consent")
                .minWidth(200)
                .cellValueFactory(new PropertyValueFactory("familyconsent"))
                .build();
        TableColumn tc17 = TableColumnBuilder.create()
                .text("Keep Data Consent")
                .minWidth(200)
                .cellValueFactory(new PropertyValueFactory("familydataconsent"))
                .build();
        TableColumn tc18 = TableColumnBuilder.create()
                .text("Patient Consent")
                .minWidth(200)
                .cellValueFactory(new PropertyValueFactory("patientconsent"))
                .build();
        consentC.getColumns().setAll(tc16, tc17, tc18);
        // Termination
        TableColumn tc19 = TableColumnBuilder.create()
                .text("Patient Termination Date")
                .minWidth(300)
                .cellValueFactory(new PropertyValueFactory("termdate"))
                .build();
        TableColumn tc20 = TableColumnBuilder.create()
                .text("Patient Termination Reason")
                .minWidth(200)
                .cellValueFactory(new PropertyValueFactory("termreason"))
                .build();
        terminationC.getColumns().setAll(tc19, tc20);
        // Mortality
        TableColumn tc23 = TableColumnBuilder.create()
                .text("Mortality")
                .minWidth(100)
                .cellValueFactory(new PropertyValueFactory("mortality"))
                .build();
        TableColumn tc24 = TableColumnBuilder.create()
                .text("Mortality Date")
                .minWidth(200)
                .cellValueFactory(new PropertyValueFactory("mortalitydate"))
                .build();
        mortalC.getColumns().setAll(tc23, tc24);
        // Severe Adverse Event
        TableColumn tc25 = TableColumnBuilder.create()
                .text("Number of Severe Adverse Event")
                .minWidth(250)
                .cellValueFactory(new PropertyValueFactory("saenum"))
                .build();
        saeC.getColumns().setAll(tc25);
        for (int date = 1; date <= 30; date++) {
            TableColumn tc = new TableColumn("date" + date);
            tc.setCellValueFactory(
                    new PropertyValueFactory<patient2, String>("date" + date));
            tc.setMinWidth(100);
            saeC.getColumns().addAll(tc);

        }

        getChildren().addAll(table);

        loadText();

        //sp.setHbarPolicy(ScrollBarPolicy.ALWAYS);
        //sp.setVbarPolicy(ScrollBarPolicy.ALWAYS);
//        ScrollPane sp = new ScrollPane();
//        sp.setFitToWidth(true);
//        sp.setFitToHeight(true);
//        sp.setPrefSize(500, 200);
//        sp.setContent(grid);
    }

    protected final synchronized void loadText() {
        ////////////////////////////
        try {

            File file = new File(PatientForm7.directory);
            file.getParentFile();
            BufferedReader text = new BufferedReader(new FileReader(file));
            String line;

            while ((line = text.readLine()) != null) {
                String[] result = line.split(",",67);
                PatientForm7.NHIbuffer.add(result[1]);
                int index = 0;
                data.add((new patient2(result[index], result[index + 1], result[index + 2],
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

                table.setItems(data);
            }
            text.close();

        } catch (IOException e) {
            System.err.println("IOException: " + e.getMessage());
        }
        /////////////////////////////////////////
    }

    public static class patient2 {

        private final SimpleStringProperty number;
        private final SimpleStringProperty nhi;
        private final SimpleStringProperty ic1;
        private final SimpleStringProperty ic2;
        private final SimpleStringProperty ic3;
        private final SimpleStringProperty ec1;
        private final SimpleStringProperty ec2;
        private final SimpleStringProperty ec3;
        private final SimpleStringProperty ec4;
        private final SimpleStringProperty ec5;
        private final SimpleStringProperty ec6;
        private final SimpleStringProperty ec7;
        private final SimpleStringProperty ec8;
        private final SimpleStringProperty ec9;
        private final SimpleStringProperty sex;
        private final SimpleStringProperty age;
        private final SimpleStringProperty pao;
        private final SimpleStringProperty fio;
        private final SimpleStringProperty spo;
        private final SimpleStringProperty ethnicity;
        private final SimpleStringProperty admission;
        private final SimpleStringProperty diagnostic;
        private final SimpleStringProperty group; // MVB or SPV
        private final SimpleStringProperty protocol; // inclusion or exlcusion

        private final SimpleStringProperty height;
        private final SimpleStringProperty weight;
        private final SimpleStringProperty apache; //Apache III 200 or 1300 code
        private final SimpleStringProperty ards;
        private final SimpleStringProperty ardsdate;
        private final SimpleStringProperty familyconsent;
        private final SimpleStringProperty familydataconsent;
        private final SimpleStringProperty patientconsent;
        private final SimpleStringProperty termdate;
        private final SimpleStringProperty termreason;
        private final SimpleStringProperty mortality;
        private final SimpleStringProperty mortalitydate;
        private final SimpleStringProperty saenum;
        private final SimpleStringProperty date1;
        private final SimpleStringProperty date2;
        private final SimpleStringProperty date3;
        private final SimpleStringProperty date4;
        private final SimpleStringProperty date5;
        private final SimpleStringProperty date6;
        private final SimpleStringProperty date7;
        private final SimpleStringProperty date8;
        private final SimpleStringProperty date9;
        private final SimpleStringProperty date10;
        private final SimpleStringProperty date11;
        private final SimpleStringProperty date12;
        private final SimpleStringProperty date13;
        private final SimpleStringProperty date14;
        private final SimpleStringProperty date15;
        private final SimpleStringProperty date16;
        private final SimpleStringProperty date17;
        private final SimpleStringProperty date18;
        private final SimpleStringProperty date19;
        private final SimpleStringProperty date20;
        private final SimpleStringProperty date21;
        private final SimpleStringProperty date22;
        private final SimpleStringProperty date23;
        private final SimpleStringProperty date24;
        private final SimpleStringProperty date25;
        private final SimpleStringProperty date26;
        private final SimpleStringProperty date27;
        private final SimpleStringProperty date28;
        private final SimpleStringProperty date29;
        private final SimpleStringProperty date30;

        public patient2(String fnumber, String fnhi, String fic1, String fic2,
                String fic3, String fec1, String fec2, String fec3, String fec4,
                String fec5, String fec6, String fec7, String fec8, String fec9,
                String fsex, String fage, String fheight, String fweight, String fpao, String ffio, String fspo,
                String fethnicity, String fadmission, String fdiagnostic,
                String fprotocol, String fgroup, String fapache, String fards, String fardsDate,
                String ffamilyconsent, String ffamilydataconsent, String fpatientconsent,
                String ftermdate, String ftermreason, String fmortality, String fmortalitydate,
                String fsaenum, String fdate1, String fdate2, String fdate3, String fdate4,
                String fdate5, String fdate6, String fdate7, String fdate8, String fdate9,
                String fdate10, String fdate11, String fdate12, String fdate13, String fdate14,
                String fdate15, String fdate16, String fdate17, String fdate18, String fdate19,
                String fdate20, String fdate21, String fdate22, String fdate23, String fdate24,
                String fdate25, String fdate26, String fdate27, String fdate28, String fdate29,
                String fdate30
        ) {
            this.number = new SimpleStringProperty(fnumber);
            this.nhi = new SimpleStringProperty(fnhi);
            this.ic1 = new SimpleStringProperty(fic1.toUpperCase());
            this.ic2 = new SimpleStringProperty(fic2.toUpperCase());
            this.ic3 = new SimpleStringProperty(fic3.toUpperCase());
            this.ec1 = new SimpleStringProperty(fec1.toUpperCase());
            this.ec2 = new SimpleStringProperty(fec2.toUpperCase());
            this.ec3 = new SimpleStringProperty(fec3.toUpperCase());
            this.ec4 = new SimpleStringProperty(fec4.toUpperCase());
            this.ec5 = new SimpleStringProperty(fec5.toUpperCase());
            this.ec6 = new SimpleStringProperty(fec6.toUpperCase());
            this.ec7 = new SimpleStringProperty(fec7.toUpperCase());
            this.ec8 = new SimpleStringProperty(fec8.toUpperCase());
            this.ec9 = new SimpleStringProperty(fec9.toUpperCase());
            this.sex = new SimpleStringProperty(fsex);
            this.age = new SimpleStringProperty(fage);
            this.height = new SimpleStringProperty(fheight);
            this.weight = new SimpleStringProperty(fweight);
            this.pao = new SimpleStringProperty(fpao);
            this.fio = new SimpleStringProperty(ffio);
            this.spo = new SimpleStringProperty(fspo);
            this.ethnicity = new SimpleStringProperty(fethnicity);
            this.admission = new SimpleStringProperty(fadmission);
            this.diagnostic = new SimpleStringProperty(fdiagnostic);
            this.group = new SimpleStringProperty(fgroup);
            this.protocol = new SimpleStringProperty(fprotocol);
            this.apache = new SimpleStringProperty(fapache);
            this.ards = new SimpleStringProperty(fards.toUpperCase());
            this.ardsdate = new SimpleStringProperty(fardsDate);
            this.familyconsent = new SimpleStringProperty(ffamilyconsent.toUpperCase());
            this.familydataconsent = new SimpleStringProperty(ffamilydataconsent.toUpperCase());
            this.patientconsent = new SimpleStringProperty(fpatientconsent.toUpperCase());
            this.termdate = new SimpleStringProperty(ftermdate);
            this.termreason = new SimpleStringProperty(ftermreason);
            this.mortality = new SimpleStringProperty(fmortality);
            this.mortalitydate = new SimpleStringProperty(fmortalitydate);
            this.saenum = new SimpleStringProperty(fsaenum);
            this.date1 = new SimpleStringProperty(fdate1);
            this.date2 = new SimpleStringProperty(fdate2);
            this.date3 = new SimpleStringProperty(fdate3);
            this.date4 = new SimpleStringProperty(fdate4);
            this.date5 = new SimpleStringProperty(fdate5);
            this.date6 = new SimpleStringProperty(fdate6);
            this.date7 = new SimpleStringProperty(fdate7);
            this.date8 = new SimpleStringProperty(fdate8);
            this.date9 = new SimpleStringProperty(fdate9);
            this.date10 = new SimpleStringProperty(fdate10);
            this.date11 = new SimpleStringProperty(fdate11);
            this.date12 = new SimpleStringProperty(fdate12);
            this.date13 = new SimpleStringProperty(fdate13);
            this.date14 = new SimpleStringProperty(fdate14);
            this.date15 = new SimpleStringProperty(fdate15);
            this.date16 = new SimpleStringProperty(fdate16);
            this.date17 = new SimpleStringProperty(fdate17);
            this.date18 = new SimpleStringProperty(fdate18);
            this.date19 = new SimpleStringProperty(fdate19);
            this.date20 = new SimpleStringProperty(fdate20);
            this.date21 = new SimpleStringProperty(fdate21);
            this.date22 = new SimpleStringProperty(fdate22);
            this.date23 = new SimpleStringProperty(fdate23);
            this.date24 = new SimpleStringProperty(fdate24);
            this.date25 = new SimpleStringProperty(fdate25);
            this.date26 = new SimpleStringProperty(fdate26);
            this.date27 = new SimpleStringProperty(fdate27);
            this.date28 = new SimpleStringProperty(fdate28);
            this.date29 = new SimpleStringProperty(fdate29);
            this.date30 = new SimpleStringProperty(fdate30);
        }

        public patient2(screeningForm.patient p) {
            this.number = new SimpleStringProperty(String.valueOf(p.m_entry));
            this.nhi = new SimpleStringProperty(p.m_nhi);
            this.ic1 = new SimpleStringProperty(String.valueOf(p.m_i1).toUpperCase());
            this.ic2 = new SimpleStringProperty(String.valueOf(p.m_i2).toUpperCase());
            this.ic3 = new SimpleStringProperty(String.valueOf(p.m_i3).toUpperCase());
            this.ec1 = new SimpleStringProperty(String.valueOf(p.m_e1).toUpperCase());
            this.ec2 = new SimpleStringProperty(String.valueOf(p.m_e2).toUpperCase());
            this.ec3 = new SimpleStringProperty(String.valueOf(p.m_e3).toUpperCase());
            this.ec4 = new SimpleStringProperty(String.valueOf(p.m_e4).toUpperCase());
            this.ec5 = new SimpleStringProperty(String.valueOf(p.m_e5).toUpperCase());
            this.ec6 = new SimpleStringProperty(String.valueOf(p.m_e6).toUpperCase());
            this.ec7 = new SimpleStringProperty(String.valueOf(p.m_e7).toUpperCase());
            this.ec8 = new SimpleStringProperty(String.valueOf(p.m_e8).toUpperCase());
            this.ec9 = new SimpleStringProperty(String.valueOf(p.m_e9).toUpperCase());
            this.sex = new SimpleStringProperty(String.valueOf(p.m_sex));
            this.age = new SimpleStringProperty(String.valueOf(p.m_age));
            this.height = new SimpleStringProperty(String.valueOf(p.m_height));
            this.weight = new SimpleStringProperty(String.valueOf(p.m_weight));
            this.pao = new SimpleStringProperty(String.valueOf(p.m_pao));
            this.fio = new SimpleStringProperty(String.valueOf(p.m_fio));
            this.spo = new SimpleStringProperty(String.valueOf(p.m_spo));
            this.ethnicity = new SimpleStringProperty(String.valueOf(p.m_ethnicity));
            this.admission = new SimpleStringProperty(String.valueOf(p.m_admissionDate));
            this.diagnostic = new SimpleStringProperty(String.valueOf(p.m_diagnostic));
            this.group = new SimpleStringProperty(String.valueOf(p.m_group));
            this.protocol = new SimpleStringProperty(String.valueOf(p.m_protocol));
            this.apache = new SimpleStringProperty(String.valueOf(p.m_apache));
            this.ards = new SimpleStringProperty(String.valueOf(p.m_ards).toUpperCase());
            this.ardsdate = new SimpleStringProperty(String.valueOf(p.m_ardsDate));
            this.familyconsent = new SimpleStringProperty(String.valueOf(p.m_famConsent).toUpperCase());
            this.familydataconsent = new SimpleStringProperty(String.valueOf(p.m_famDataConsent).toUpperCase());
            this.patientconsent = new SimpleStringProperty(String.valueOf(p.m_patientConsent).toUpperCase());
            this.termdate = new SimpleStringProperty(String.valueOf(p.m_termdate));
            this.termreason = new SimpleStringProperty(String.valueOf(p.m_termreason));
            this.mortality = new SimpleStringProperty(String.valueOf(p.m_mortality));
            this.mortalitydate = new SimpleStringProperty(String.valueOf(p.m_mortalitydate));
            this.saenum = new SimpleStringProperty(String.valueOf(p.m_saenum));
            this.date1 = new SimpleStringProperty(String.valueOf(p.m_date1));
            this.date2 = new SimpleStringProperty(String.valueOf(p.m_date2));
            this.date3 = new SimpleStringProperty(String.valueOf(p.m_date3));
            this.date4 = new SimpleStringProperty(String.valueOf(p.m_date4));
            this.date5 = new SimpleStringProperty(String.valueOf(p.m_date5));
            this.date6 = new SimpleStringProperty(String.valueOf(p.m_date6));
            this.date7 = new SimpleStringProperty(String.valueOf(p.m_date7));
            this.date8 = new SimpleStringProperty(String.valueOf(p.m_date8));
            this.date9 = new SimpleStringProperty(String.valueOf(p.m_date9));
            this.date10 = new SimpleStringProperty(String.valueOf(p.m_date10));
            this.date11 = new SimpleStringProperty(String.valueOf(p.m_date11));
            this.date12 = new SimpleStringProperty(String.valueOf(p.m_date12));
            this.date13 = new SimpleStringProperty(String.valueOf(p.m_date13));
            this.date14 = new SimpleStringProperty(String.valueOf(p.m_date14));
            this.date15 = new SimpleStringProperty(String.valueOf(p.m_date15));
            this.date16 = new SimpleStringProperty(String.valueOf(p.m_date16));
            this.date17 = new SimpleStringProperty(String.valueOf(p.m_date17));
            this.date18 = new SimpleStringProperty(String.valueOf(p.m_date18));
            this.date19 = new SimpleStringProperty(String.valueOf(p.m_date19));
            this.date20 = new SimpleStringProperty(String.valueOf(p.m_date20));
            this.date21 = new SimpleStringProperty(String.valueOf(p.m_date21));
            this.date22 = new SimpleStringProperty(String.valueOf(p.m_date22));
            this.date23 = new SimpleStringProperty(String.valueOf(p.m_date23));
            this.date24 = new SimpleStringProperty(String.valueOf(p.m_date24));
            this.date25 = new SimpleStringProperty(String.valueOf(p.m_date25));
            this.date26 = new SimpleStringProperty(String.valueOf(p.m_date26));
            this.date27 = new SimpleStringProperty(String.valueOf(p.m_date27));
            this.date28 = new SimpleStringProperty(String.valueOf(p.m_date28));
            this.date29 = new SimpleStringProperty(String.valueOf(p.m_date29));
            this.date30 = new SimpleStringProperty(String.valueOf(p.m_date30));
        }
        ////////////////////////// SAE Date 20- 30/////////////////////////////////////
        public String getDate30() {
            return date30.get();
        }

        public void setDate30(String fdate30) {
            date30.set(fdate30);
        }

        public String getDate29() {
            return date29.get();
        }

        public void setDate29(String fdate29) {
            date29.set(fdate29);
        }

        public String getDate28() {
            return date28.get();
        }

        public void setDate28(String fdate28) {
            date28.set(fdate28);
        }

        public String getDate27() {
            return date27.get();
        }

        public void setDate27(String fdate27) {
            date27.set(fdate27);
        }

        public String getDate26() {
            return date26.get();
        }

        public void setDate26(String fdate26) {
            date26.set(fdate26);
        }

        public String getDate25() {
            return date25.get();
        }

        public void setDate25(String fdate25) {
            date25.set(fdate25);
        }

        public String getDate24() {
            return date24.get();
        }

        public void setDate24(String fdate24) {
            date24.set(fdate24);
        }
        
        public String getDate23() {
            return date23.get();
        }

        public void setDate23(String fdate23) {
            date23.set(fdate23);
        }

        public String getDate22() {
            return date22.get();
        }

        public void setDate22(String fdate22) {
            date22.set(fdate22);
        }
        
        public String getDate21() {
            return date21.get();
        }

        public void setDate21(String fdate21) {
            date21.set(fdate21);
        }
        ////////////////////////// SAE Date 10- 20/////////////////////////////////////
        public String getDate20() {
            return date20.get();
        }

        public void setDate20(String fdate20) {
            date20.set(fdate20);
        }

        public String getDate19() {
            return date19.get();
        }

        public void setDate19(String fdate19) {
            date19.set(fdate19);
        }

        public String getDate18() {
            return date18.get();
        }

        public void setDate18(String fdate18) {
            date18.set(fdate18);
        }

        public String getDate17() {
            return date17.get();
        }

        public void setDate17(String fdate17) {
            date17.set(fdate17);
        }

        public String getDate16() {
            return date16.get();
        }

        public void setDate16(String fdate16) {
            date16.set(fdate16);
        }

        public String getDate15() {
            return date15.get();
        }

        public void setDate15(String fdate15) {
            date15.set(fdate15);
        }

        public String getDate14() {
            return date14.get();
        }

        public void setDate14(String fdate14) {
            date14.set(fdate14);
        }

        public String getDate13() {
            return date13.get();
        }

        public void setDate13(String fdate13) {
            date13.set(fdate13);
        }

        public String getDate12() {
            return date12.get();
        }

        public void setDate12(String fdate12) {
            date12.set(fdate12);
        }

        public String getDate11() {
            return date11.get();
        }

        public void setDate11(String fdate11) {
            date11.set(fdate11);
        }

        //////////////////////////////////////////////////////////////////////////////
        ////////////////////////// SAE Date 1- 10/////////////////////////////////////

        public String getDate10() {
            return date10.get();
        }

        public void setDate10(String fdate10) {
            date10.set(fdate10);
        }

        public String getDate9() {
            return date9.get();
        }

        public void setDate9(String fdate9) {
            date9.set(fdate9);
        }

        public String getDate8() {
            return date8.get();
        }

        public void setDate8(String fdate8) {
            date8.set(fdate8);
        }

        public String getDate7() {
            return date7.get();
        }

        public void setDate7(String fdate7) {
            date7.set(fdate7);
        }

        public String getDate6() {
            return date6.get();
        }

        public void setDate6(String fdate6) {
            date6.set(fdate6);
        }

        public String getDate5() {
            return date5.get();
        }

        public void setDate5(String fdate5) {
            date5.set(fdate5);
        }

        public String getDate4() {
            return date4.get();
        }

        public void setDate4(String fdate4) {
            date4.set(fdate4);
        }

        public String getDate3() {
            return date3.get();
        }

        public void setDate3(String fdate3) {
            date3.set(fdate3);
        }

        public String getDate2() {
            return date2.get();
        }

        public void setDate2(String fdate2) {
            date2.set(fdate2);
        }

        public String getDate1() {
            return date1.get();
        }

        public void setDate1(String fdate1) {
            date1.set(fdate1);
        }
        /////////////////////////////////////////////////////////////////////

        public String getSaenum() {
            return saenum.get();
        }

        public void setSaenum(String fsaenum) {
            saenum.set(fsaenum);
        }

        public String getMortalitydate() {
            return mortalitydate.get();
        }

        public void setMortalitydate(String fmortalitydate) {
            mortalitydate.set(fmortalitydate);
        }

        public String getMortality() {
            return mortality.get();
        }

        public void setMortality(String fmortality) {
            mortality.set(fmortality);
        }

        public String getTermreason() {
            return termreason.get();
        }

        public void setTermreason(String ftermreason) {
            termreason.set(ftermreason);
        }

        public String getTermdate() {
            return termdate.get();
        }

        public void setTermdate(String ftermdate) {
            termdate.set(ftermdate);
        }

        public String getPatientconsent() {
            return patientconsent.get();
        }

        public void setPatientconsent(String fpatientconsent) {
            patientconsent.set(fpatientconsent);
        }

        public String getFamilydataconsent() {
            return familydataconsent.get();
        }

        public void setFamilydataconsent(String ffamilydataconsent) {
            familydataconsent.set(ffamilydataconsent);
        }

        public String getFamilyconsent() {
            return familyconsent.get();
        }

        public void setFamilyconsent(String ffamilyconsent) {
            familyconsent.set(ffamilyconsent);
        }

        public String getArdsdate() {
            return ardsdate.get();
        }

        public void setArdsdate(String fardsDate) {
            ardsdate.set(fardsDate);
        }

        public String getArds() {
            return ards.get();
        }

        public void setArds(String fards) {
            ards.set(fards);
        }

        public String getApache() {
            return apache.get();
        }

        public void setApache(String fapache) {
            apache.set(fapache);
        }

        public String getWeight() {
            return weight.get();
        }

        public void setWeight(String fweight) {
            weight.set(fweight);
        }

        public String getHeight() {
            return height.get();
        }

        public void setHeight(String fheight) {
            height.set(fheight);
        }

        public String getDiagnostic() {
            return diagnostic.get();
        }

        public void setDiagnostic(String fdiagnostic) {
            diagnostic.set(fdiagnostic);
        }

        public String getAdmission() {
            return admission.get();
        }

        public void setAdmission(String fadmission) {
            admission.set(fadmission);
        }

        public String getEthnicity() {
            return ethnicity.get();
        }

        public void setEthnicity(String fethnicity) {
            ethnicity.set(fethnicity);
        }

        public String getSpo() {
            return spo.get();
        }

        public void setSpo(String fspo) {
            spo.set(fspo);
        }

        public String getFio() {
            return fio.get();
        }

        public void setFio(String ffio) {
            fio.set(ffio);
        }

        public String getPao() {
            return pao.get();
        }

        public void setPao(String fpao) {
            pao.set(fpao);
        }

        public String getAge() {
            return age.get();
        }

        public void setAge(String fage) {
            age.set(fage);
        }

        public String getSex() {
            return sex.get();
        }

        public void setSex(String fsex) {
            sex.set(fsex);
        }

        public String getProtocol() {
            return protocol.get();
        }

        public void setProtocol(String fprotocol) {
            protocol.set(fprotocol);
        }

        public String getGroup() {
            return group.get();
        }

        public void setGroup(String fgroup) {
            group.set(fgroup);
        }

        public String getNumber() {
            return number.get();
        }

        public void setNumber(String fnumber) {
            number.set(fnumber);
        }

        public String getNhi() {
            return nhi.get();
        }

        public void setNhi(String fnhi) {
            nhi.set(fnhi);
        }

        public String getIc1() {
            return ic1.get();
        }

        public void setIc1(String fic1) {
            ic1.set(fic1);
        }

        public String getIc2() {
            return ic2.get();
        }

        public void setIc2(String fic2) {
            ic2.set(fic2);
        }

        public String getIc3() {
            return ic3.get();
        }

        public void setIc3(String fic3) {
            ic3.set(fic3);
        }

        public String getEc1() {
            return ec1.get();
        }

        public void setEc1(String fec1) {
            ec1.set(fec1);
        }

        public String getEc2() {
            return ec2.get();
        }

        public void setEc2(String fec2) {
            ec2.set(fec2);
        }

        public String getEc3() {
            return ec3.get();
        }

        public void setEc3(String fec3) {
            ec3.set(fec3);
        }

        public String getEc4() {
            return ec4.get();
        }

        public void setEc4(String fec4) {
            ec4.set(fec4);
        }

        public String getEc5() {
            return ec5.get();
        }

        public void setEc5(String fec5) {
            ec5.set(fec5);
        }

        public String getEc6() {
            return ec6.get();
        }

        public void setEc6(String fec6) {
            ec6.set(fec6);
        }

        public String getEc7() {
            return ec7.get();
        }

        public void setEc7(String fec7) {
            ec7.set(fec7);
        }

        public String getEc8() {
            return ec8.get();
        }

        public void setEc8(String fec8) {
            ec8.set(fec8);
        }

        public String getEc9() {
            return ec9.get();
        }

        public void setEc9(String fec9) {
            ec9.set(fec9);
        }
    }
}
