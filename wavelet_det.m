function r = wavelet_det(x, fs)
x = x(:)';
w = modwt(x, 'sym4', 5);
mra = modwtmra(w, 'sym4');
f = sum(mra(4:5, :), 1);
env = movmean(f .^ 2, round(0.05 * fs));
thr = 0.3 * prctile(env, 99.5);
[~, loc] = findpeaks(env, 'MinPeakHeight', thr, ...
                     'MinPeakDistance', round(0.25 * fs));

[b2, a2] = butter(4, [0.5 40] / (fs/2), 'bandpass');
y = filtfilt(b2, a2, x);
h = round(0.1 * fs);
r = zeros(size(loc));
for k = 1:numel(loc)
    lo = max(1, loc(k) - h);
    hi = min(numel(y), loc(k) + h);
    [~, i] = max(y(lo:hi));
    r(k) = lo + i - 1;
end
end