function table = BitwiseToLBP
    % we reserve label 0 for non-uniform
    table = zeros(1, 256);
    nextLabel = 1;
    for k = 1:256,
        bits = bitand(k, 2.^(0:7)) > 0;
        if IsUniformLBP(bits),
            table(k) = nextLabel;
            nextLabel = nextLabel + 1;
        else
            table(k) = 0;
        end
    end
end

function x = IsUniformLBP(bits)
    x = nnz(diff(bits([1:end, 1]))) == 2;
end