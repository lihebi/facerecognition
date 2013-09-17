function AH = test()
	db=database('test','hebi','','com.mysql.jdbc.Driver','jdbc:mysql://127.0.0.1:3306/test');
	load('myah.mat');
	writer = fopen('sql.txt','w');
	for i=1:size(myah, 3)%1000
		tic;
		for j=1:size(myah, 1)%59
			sql = sprintf('insert into matlab values(%d, %d', i, j);
			for k = 1:size(myah, 2)%760
				sql = sprintf('%s, %f', sql, myah(j, k, i));
			end
			sql = [sql, ')'];
			%exec(db, sql);
			fprintf(writer, '%s\n', sql);
		end
		toc;
	end
end
function AH = myload(index)
	load(['data/AH', int2str(index), '.mat']);
end
