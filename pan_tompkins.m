function r = pan_tompkins(x, fs)
x = x(:)';
[b, a] = butter(2, [5 15] / (fs/2), 'bandpass');
f = filtfilt(b, a, x);
sq = [0 diff(f)] .^ 2;
m = movmean(sq, round(0.15 * fs));
thr = 0.35 * prctile(m, 99.5);
[~, loc] = findpeaks(m, 'MinPeakHeight', thr, ...
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