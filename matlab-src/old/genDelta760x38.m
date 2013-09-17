function matrix = genDelta760x38()
	matrix = [];
	for i=1:38
		tmp = zeros(760, 1);
		for j=(i-1)*20+1: i*20
			tmp(j) = 1;
		end
		matrix = [matrix; tmp];
	end
	disp(size(matrix));
end
