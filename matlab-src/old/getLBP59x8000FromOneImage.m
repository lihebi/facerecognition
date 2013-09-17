function getLBP59x8000FromOneImage(image)
	patches = getDivide();
	table = BitwiseToLBP();
	vector59x8000 = [];
	for i=1:size(patches, 1)
		vector59x1 = calPatchLBP(image, patches(i, :), table);
		vector59x8000 = [vector59x8000, vector59x1];
	end
end
