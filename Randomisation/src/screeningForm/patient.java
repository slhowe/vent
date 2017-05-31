/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package screeningForm;

import eu.schudt.javafx.controls.calendar.DatePicker;
import java.text.SimpleDateFormat;
import javafx.scene.control.CheckBox;
import javafx.scene.control.TextField;

/**
 *
 * @author ktk15
 */
public class patient {

    public int m_entry;
    public String m_nhi;
    public String m_sex;
    public int m_age;
    public float m_pao;
    public float m_fio;
    public float m_spo;
    public String m_diagnostic;
    public String m_ethnicity;
    public String m_admissionDate;
    public boolean m_i1;
    public boolean m_i2;
    public boolean m_i3;
    public boolean m_e1;
    public boolean m_e2;
    public boolean m_e3;
    public boolean m_e4;
    public boolean m_e5;
    public boolean m_e6;
    public boolean m_e7;
    public boolean m_e8;
    public boolean m_e9;
    public String m_group;
    public String m_protocol;
    public String m_height = "";
    public String m_weight= "";
    public String m_apache = "";
    public boolean m_ards = false;
    public String m_ardsDate = "";

    public String m_famConsent="";
    public String m_famDataConsent = "";
    public String m_patientConsent = "";
    public String m_termdate = "";
    public String m_termreason = "";
    public boolean m_mortality = false;
    public String m_mortalitydate = "";
    public int m_saenum = 0;
    public String m_date1 = "";
    
    public String m_date2 = "";
    public String m_date3 = "";
    public String m_date4 = "";
    public String m_date5 = "";
    public String m_date6 = "";
    public String m_date7 = "";
    public String m_date8 = "";
    public String m_date9 = "";
    public String m_date10 = "";
    public String m_date11 = "";
    public String m_date12 = "";
    public String m_date13 = "";
    public String m_date14 = "";
    public String m_date15 = "";
    public String m_date16 = "";
    public String m_date17 = "";
    public String m_date18 = "";
    public String m_date19 = "";
    public String m_date20 = "";
    public String m_date21 = "";
    public String m_date22 = "";
    public String m_date23 = "";
    public String m_date24 = "";
    public String m_date25 = "";
    public String m_date26 = "";
    public String m_date27 = "";
    public String m_date28 = "";
    public String m_date29 = "";
    public String m_date30 = "";
    
    
    

    /*
     , TextField TF4,
     TextField TF5, TextField TF6, TextField TF7,
     TextField TF8, TextField TF9
     */

    public patient(int pNumber, TextField TF1, TextField TF2, TextField TF3, TextField TF4,
            TextField TF5, TextField TF6, TextField TF7, DatePicker TF8, TextField TF9,
            CheckBox cbi1, CheckBox cbi2, CheckBox cbi3, CheckBox cbe1, CheckBox cbe2,
            CheckBox cbe3, CheckBox cbe4, CheckBox cbe5, CheckBox cbe6,
            CheckBox cbe7, CheckBox cbe8, CheckBox cbe9) {
        //m_entry = number;
        SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yy");
        m_nhi = TF1.getText().toUpperCase();
        m_i1 = cbi1.isSelected();
        m_i2 = cbi2.isSelected();
        m_i3 = cbi3.isSelected();
        m_e1 = cbe1.isSelected();
        m_e2 = cbe2.isSelected();
        m_e3 = cbe3.isSelected();
        m_e4 = cbe4.isSelected();
        m_e5 = cbe5.isSelected();
        m_e6 = cbe6.isSelected();
        m_e7 = cbe7.isSelected();
        m_e8 = cbe8.isSelected();
        m_e9 = cbe9.isSelected();
        m_entry = pNumber;

        m_sex = TF2.getText().toUpperCase();
        m_age = Integer.parseInt(TF3.getText());
       

        m_pao = Float.parseFloat(TF4.getText());
        m_fio = Float.parseFloat(TF5.getText());
        m_spo = Float.parseFloat(TF6.getText());
        m_ethnicity = TF7.getText();
        m_admissionDate = formatter.format(TF8.getSelectedDate());
        m_diagnostic = TF9.getText();

    }

}
