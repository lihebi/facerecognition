function AH = lihebi()
% 1. use this to generate AH
% 2. use l1min to gen positive and negtive, create finalR.mat, which is
% feature data.
% 3. use genY to gen Y.mat, which is classify data.
% 4. use adaBoost
end
function loadThe9th()
    AH = {};
    data = dir('./lbpdata/');
    for i=1:460
        AH{i} = [];
    end
    count=0;
    for i=data'
        if i.name == '.', continue; end
        load(strcat('./lbpdata/', i.name));
        for ii=1:460
            AH{ii} = [AH{ii}, vector59x8000(:, ii+8000)];
        end
        count = count+1;
        disp(count);
    end
    save('AH9.mat', 'AH');
end
function loadAllMatPartly(step)
    data = dir('./lbpdata/');
    for i=1:9
        loadPart(step, i);
        disp(i);
    end
end
function loadPart(step, index)
    data = dir('./lbpdata/');
    AH = reloadAH();
    count=0;
    for i=data'
        if i.name=='.', continue; end
        load(strcat('./lbpdata/', i.name));
        for ii=1:step
            AH{ii} = [AH{ii}, vector59x8000(:, ii+(index-1)*step)];
        end
        count=count+1;
        disp(count);
    end
    saveAH(AH, index);
end
function AH = reloadAH()
    AH = {};
    for i=1:1000
        AH{i} = [];
    end
end
function saveAH(AH, index)
    save(strcat('AH', num2str(index), '.mat'), 'AH');
end
function AH=genAHFromData()
    AH = {};
    data = dir('./lbpdata/');
    for i=data'
        if i.name=='.', continue; end
        disp(i.name);
        load(strcat('./lbpdata/', i.name));
        if ~size(AH)
            for ii=1:size(vector59x8000, 2)
                AH{ii} = [];
            end
        end
        for ii=1:size(vector59x8000, 2)
            AH{ii} = [AH{ii}, vector59x8000(:, ii)];
        end
        disp(size(AH{1}));
    end
end
function AH = getAllAH()
    AH = {};
    patches = getDivide();
    table = BitwiseToLBP();
    trainingSet = dir('~/YaleB/training/');
    count=0;
    for i=trainingSet'
        count = count+1;
        disp(count);
        if i.name=='.', continue; end
        image = imread(strcat('~/YaleB/training/', i.name));
        vector59x8000 = getLBPFromOneImage(image, patches, table);
        save(strcat('./lbpdata/', i.name, '.mat'), 'vector59x8000');
    end
end
function vector59x8000 = getLBPFromOneImage(image, patches, table)
    vector59x8000 = [];
    for i=1:size(patches, 1)
        vector59x1 = calPatchLBP(image, patches(i, :), table);
        vector59x8000 = [vector59x8000, vector59x1];
    end
end
function genBlur()
    blurSrcSet = dir('~/YaleB/blur_src/');
    for pa=blurSrcSet'
        if pa.name=='.', continue; end
        image = imread(strcat('~/YaleB/blur_src/', pa.name));
        image2 = imnoise(image);
        imwrite(image2, strcat('~/YaleB/blur/',pa.name));
    end
end
