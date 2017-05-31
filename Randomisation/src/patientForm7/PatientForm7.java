/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package patientForm7;

import addInfo.AddInfoPane;
import screeningForm.ScreeningFormPane;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.ArrayList;
import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.scene.layout.BorderPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import patientInfo.PatientInfoPane;


/**
 *
 * @author ktk15
 */
public class PatientForm7 extends Application {
    public static int patientNumber;
    //public static String directory= "D:\\MV\\Clinical\\Screening Protocol\\JAVA\\test.csv";
    public static String directory= "patientData.csv";
    public static String tempdirectory= "tempPatientData.csv";
    public static boolean buttonPressed = false;
    public ScreeningFormPane screeningForm;
    public PatientInfoPane patientInfoPane;
    public AddInfoPane AddInfoPane;
    //public AdditionalInfoPane additionalInfoPane;
    public static ArrayList<String> NHIbuffer = new ArrayList();

    
    public void createTxtFile() {
        try {

            File file = new File(directory);
            file.getParentFile();

            // if file doesnt exists, then create it
            if (!file.exists()) {
                file.createNewFile();
            }
            LineNumberReader lnr = new LineNumberReader(new FileReader(file));
            lnr.skip(Long.MAX_VALUE);
            
            // Finally, the LineNumberReader object should be closed to prevent resource leak
            lnr.close();
            patientNumber =  lnr.getLineNumber()+1;
            


        } catch (IOException e) {
            e.printStackTrace();
        }

    }
   
    
    @Override
    public void start(Stage primaryStage) {
       createTxtFile();
       
        primaryStage.setTitle("Screening and Randomisation Sheet");
        Group root = new Group();
        Scene scene = new Scene(root, 1800, 1000, Color.WHITE);
        TabPane tabPane = new TabPane();

        BorderPane borderPane = new BorderPane();
        
        
        Tab tabScreening = new Tab();
        final ScrollPane spScreening = new ScrollPane();
        final ScrollPane spAdd = new ScrollPane();
        //final ScrollPane sp3 = new ScrollPane();
        
        tabScreening.setClosable(false);
        tabScreening.setText("Screening Form");
        spScreening.setContent( screeningForm = new ScreeningFormPane( this ));
        tabScreening.setContent(spScreening);
        
        Tab tabPatientInfo = new Tab();
        tabPatientInfo.setClosable(false);
        tabPatientInfo.setText("Patient Information");
        tabPatientInfo.setContent( patientInfoPane = new PatientInfoPane( this ) );
        Tab tabAdditionalInfo = new Tab();
        tabAdditionalInfo.setClosable(false);
        tabAdditionalInfo.setText("Additional Information");
        spAdd.setContent(AddInfoPane = new AddInfoPane(this));
        tabAdditionalInfo.setContent(spAdd);
        
        tabPane.getTabs().add(tabScreening);
        tabPane.getTabs().add(tabPatientInfo);
        tabPane.getTabs().add(tabAdditionalInfo);

        // bind to take available space
        borderPane.prefHeightProperty().bind(scene.heightProperty());
        borderPane.prefWidthProperty().bind(scene.widthProperty());

        borderPane.setCenter(tabPane);
        root.getChildren().add(borderPane);
        scene.getStylesheets().add(PatientForm7.class.getResource("calendar.css").toExternalForm());
        primaryStage.setScene(scene);
        primaryStage.show();
        
        
       
    }
    

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        launch(args);
    }
    
}
