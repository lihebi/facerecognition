function vector59x1 = calPatchLBP(image, patch, table)
%table([1:256])={0 for non-uniform, 1-58 for other}
    xstart=patch(1);xend=patch(2);ystart=patch(3);yend=patch(4);
    x=xstart;y=ystart;
    vector = zeros(1,59);
    while(x<xend)
        while(y<yend)
            lbp = (table(calLBP(image, x, y)));
            vector(lbp+1) = vector(lbp+1)+1; %vector([1:59]), 1 for non-uniform, 2-59 for other
            y = y+1;           
        end
        x = x+1;
    end
    vector = normalVector(vector);
    vector59x1 = vector';
end
function vector = normalVector(v)
    sum=0;
    vector = zeros(1,length(v));
    for pa=1:length(v)
        sum = sum+v(pa);
    end
    for pa=1:length(v)
        vector(pa) = v(pa)/sum;
    end
end
function lbp=calLBP(image, x, y)
%normal for 1 to 255, 256 for 0
    center=image(x,y);
    lbp=0;
    lbp = lbp+bitshift(double(image(x-1,y-1)>center), 7);
    lbp = lbp+bitshift(double(image(x-1,y  )>center), 6);
    lbp = lbp+bitshift(double(image(x-1,y+1)>center), 5);
    lbp = lbp+bitshift(double(image(x  ,y-1)>center), 4);
    lbp = lbp+bitshift(double(image(x  ,y+1)>center), 3);
    lbp = lbp+bitshift(double(image(x+1,y-1)>center), 2);
    lbp = lbp+bitshift(double(image(x+1,y  )>center), 1);
    lbp = lbp+bitshift(double(image(x+1,y+1)>center), 0);
    if lbp==0, lbp=256;end
end