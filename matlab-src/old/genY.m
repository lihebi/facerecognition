function genY()
    Y = [];
    blurSet = dir('~/YaleB/blur/');
    for i=blurSet'
        if i.name=='.', continue; end
        Y = [Y, gen(i.name)];
    end
    save('Y.mat', Y);
end

function gen(name)
    result = zeros(1,38);
    for i=1:38
        if i<10, strtmp = strcat('0', num2str(i));
        elseif i<14, strtmp = num2str(i);
        else, strtmp = num2str(i+1);
        end
        strtmp = strcat('B', strtmp);
        if findstr(name, strtmp)
            result(i)=1;
            return;
        end
    end
end