load data/mat/b001.mat
fs = double(fs);
ecg = I(:)';
t = (1:length(ecg)) / fs;

[b, a] = butter(4, [0.5 40] / (fs/2), 'bandpass');
y = filtfilt(b, a, ecg);

seg = t < 10;
plot(t(seg), ecg(seg), 'Color', [0.7 0.7 0.7]); hold on
plot(t(seg), y(seg), 'k');
legend('raw', 'Butterworth 0.5-40 Hz');
xlabel('time (s)'); ylabel('mV');