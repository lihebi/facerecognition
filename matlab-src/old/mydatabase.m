function mydatabase()
    createSQLFile(4, 'sql4000.txt');
end
function createSQLFile(index, txtname)
	matFilename = sprintf('data/AH%d.mat', index);
	writer = fopen(txtname, 'w');
	load(matFilename);
	for i=1:size(AH, 2)%1000
		disp(i);
		tic;
		for j=1:size(AH{i}, 1)%59
			sql = sprintf('insert into matlab values(%d, %d', i, j);
			for k=1:size(AH{i}, 2)%760
				sql = sprintf('%s, %f', sql, AH{i}(j, k));
			end
			sql = [sql, ')'];
			fprintf(writer, '%s\n', sql);
		end
		toc;
	end
end
