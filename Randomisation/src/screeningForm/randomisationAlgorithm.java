/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package screeningForm;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/**
 *
 * @author ktk15
 */
public class randomisationAlgorithm{
    String m_groupString;

    public randomisationAlgorithm(boolean InclusionCriteria) throws IOException {
        if (InclusionCriteria == true){
            
        
        String directory = "Currentstate.csv";
        int[] Block = new int[10];
        int[] CurrentState = new int[15];
        int blockr = 0;
        int randBlock = BlockSize(blockr);
        File file = new File(directory);
        file.getParentFile();
        if (!file.exists()) {
            try {

                file.createNewFile();

                for (int i = 0; i <= 4; i++) {
                    CurrentState[i] = 1;
                }
                getCurrentState(CurrentState, Block, randBlock);
                PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(directory, true)));
                for (int k = 0; k <= 14; k++) {
                    out.printf("%d,", CurrentState[k]);
                }
                out.close();

            } catch (IOException e) {
                e.printStackTrace();
            }
        } else {
            try {
                BufferedReader text = new BufferedReader(new FileReader(file));

                String Line = text.readLine();
                String[] result = Line.split(",");

                for (int i = 0; i < 15; i++) {

                    CurrentState[i] = Integer.parseInt(result[i]);
                }
            } catch (FileNotFoundException ex) {
           
                
            }

        }

        // Start of new block
        if (CurrentState[2] > CurrentState[3]) {
            //System.out.println("START NEW");
            getCurrentState(CurrentState, Block, randBlock);
            CurrentState[4] += 1;
            CurrentState[2] = 1;
        }

        RCTState state = new RCTState(CurrentState);
        if (state.m_Block[state.m_CurrentBlockPosition - 1] == 1) {
            //System.out.println(String.format("MBV-%03d", state.m_InterventionN));
            m_groupString = String.format("MBV-%03d", state.m_InterventionN);
            state.m_InterventionN += 1;
        } else if (state.m_Block[state.m_CurrentBlockPosition - 1] == 0) {
            //System.out.println(String.format("SPV-%03d", state.m_ControlN));
            m_groupString=(String.format("SPV-%03d", state.m_ControlN));
            state.m_ControlN += 1;
        }
        state.m_CurrentBlockPosition += 1;
        System.out.println(m_groupString);
        try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(directory)))) {
            out.write(String.format("%d,", state.m_InterventionN));
            out.write(String.format("%d,", state.m_ControlN));

            out.printf("%d,", state.m_CurrentBlockPosition);
            out.printf("%d,", state.m_CurrentBlockSize);
            out.printf("%d,", state.m_BlockNumber);
            for (int k = 0; k < 10; k++) {
                out.printf("%d,", state.m_Block[k]);
            }
        }
        }
        else if (InclusionCriteria == false){
            m_groupString = "N/A";
        }
    }

    /**
     * @param args the command line arguments
     */
    private void RandPerm(int[] Block, int currentBlockSize) {
        List<Double> resultF = new ArrayList<Double>(currentBlockSize);

        for (int j = 1; j <= currentBlockSize; j++) {

            double k = Math.round((j - 1.0) / currentBlockSize);
            resultF.add(k);

        }

        Collections.shuffle(resultF);
        for (int k = 0; k <= currentBlockSize - 1; k++) {
            Block[k] = resultF.get(k).intValue();
        }
        
    }

    private void getCurrentState(int[] CurrentState, int[] Block, int currentBlockSize) {
        CurrentState[3] = currentBlockSize;
        RandPerm(Block, currentBlockSize);
        for (int j = 5; j <= 14; j++) {
            int i = j - 5;
            CurrentState[j] = Block[i];

        }
        //System.out.println("CurrentState  ");
        //System.out.printf(Arrays.toString(CurrentState));
    }

    private int BlockSize(int blockr) {
        Random rnd = new Random();
        int[] BlockSize = new int[3];
        BlockSize[0] = 4;
        BlockSize[1] = 6;
        BlockSize[2] = 8;
        blockr = BlockSize[rnd.nextInt(3)];
        return blockr;

    }

}
