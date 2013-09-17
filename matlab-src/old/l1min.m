function AH=l1min()
	db=database('test','hebi','','com.mysql.jdbc.Driver','jdbc:mysql://127.0.0.1:3306/test');
    AH=loadAH();
    finalR = calL1For8000AHs(AH);
    %8460* 38*800
    save('finalR.mat', 'finalR');
end
function finalR = calL1For8000AHs(AH)
    finalR = [];
    %should use 8000 AHs
    for i=1:1000
        rRow = calL1ForSingleAH(AH{i}, i);
        finalR = [finalR; rRow];
    end
end
function r = calL1ForSingleAH(AH, index)
    r = solveXFor800Blurs(AH, index);
end
function rVector1x38x800 = solveXFor800Blurs(AH, index)
    rVector1x38x800 = [];
    patches = getDivide();
    table = BitwiseToLBP();
    blurSet = dir('~/YaleB/blur/');
    for i=blurSet'
        if i.name=='.', continue; end
        image = imread(strcat('~/YaleB/blur/', i.name));
        [l,x]=solveXForSingleBlur(image, patches(index, :), table);
        rVector1x38 = cal38Ris(l,x,AH);
        rVector1x38x800 = [rVector1x38x800, rVector1x38];
    end
end
function [vector59x1, x]=solveForSingleBlur(image, patch, table)
    vector59x1 = calPatchLBP(image, patches(index, :), table);
    x = solveX(AH, vector59x1);
end
function x = solveX(AH, y)
    epsilon = 0.05;
    x0 = AH'*y;
    xp = l1qc_logbarrier(x0, AH, [], y, epsilon, 1e-3);
end
function rVector1x38 = cal38Ris(l, x, AH)
    rVector1x38 = [];
    for i=1:38
        del = delta(i);
        r = norm((l-AH*del), 2);
        rVector1x38 = [rVector1x38, r];
    end
end

function AH=loadAH()
    load('AH1.mat');
end
