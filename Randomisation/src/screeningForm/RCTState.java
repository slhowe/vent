/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package screeningForm;


/**
 *
 * @author ktk15
 */
public class RCTState {
    int m_InterventionN;
    int m_ControlN;
    int m_CurrentBlockPosition;
    int m_CurrentBlockSize;
    int m_BlockNumber;
    /*
    int m_CurrentBlock1;
    int m_CurrentBlock2;
    int m_CurrentBlock3;
    int m_CurrentBlock4;
    int m_CurrentBlock5;
    int m_CurrentBlock6;
    int m_CurrentBlock7;
    int m_CurrentBlock8;
    int m_CurrentBlock9;
    int m_CurrentBlock10;
    */
    int[] m_Block = new int[10];
    
    public RCTState(int[] CurrentState){
         m_InterventionN = CurrentState[0];
        m_ControlN = CurrentState[1];
        m_CurrentBlockPosition = CurrentState[2];
        m_CurrentBlockSize =CurrentState[3];
        m_BlockNumber=CurrentState[4];
        /*
        m_CurrentBlock1=CurrentState[5];
        m_CurrentBlock2=CurrentState[6];
        m_CurrentBlock3=CurrentState[7];
        m_CurrentBlock4=CurrentState[8];
        m_CurrentBlock5=CurrentState[9];
        m_CurrentBlock6=CurrentState[10];
        m_CurrentBlock7=CurrentState[11];
        m_CurrentBlock8=CurrentState[12];
        m_CurrentBlock9=CurrentState[13];
        m_CurrentBlock10=CurrentState[14];
        */
        for (int i = 5;i<15;i++){
            m_Block[i-5] = CurrentState[i];
        }
       
    }
}
