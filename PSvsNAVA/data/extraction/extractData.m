function extractData(file)
    load(file)

    i = findstr(file, '.');
    filename = file(1:i-1)

    % save flow
    savefile = [filename '_flow.csv'];
    fid = fopen(savefile, 'wt');
    for index = 1:length(flow)
        fprintf(fid, '%f\n', flow(index))
    end
    fclose(fid);
    printf('File %s created\n', savefile)

    %save pres
    savefile = [filename '_pres.csv'];
    fid = fopen(savefile, 'wt');
    for index = 1:length(press)
        fprintf(fid, '%f\n', press(index))
    end
    fclose(fid);
    printf('File %s created\n', savefile)

    %save eadi
    savefile = [filename '_eadi.csv'];
    fid = fopen(savefile, 'wt');
    for index = 1:length(eadi)
        fprintf(fid, '%f\n', eadi(index))
    end
    fclose(fid);
    printf('File %s created\n', savefile)

end
