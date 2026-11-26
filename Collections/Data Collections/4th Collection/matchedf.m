function [y] = matchedf(sig,ref)
ref = flipud(ref);
y = conv(sig,ref);
end