samples = 2e6;
samples_per_increment = 16;
initial_samples = samples/samples_per_increment-1;

AOM_Trace = zeros(initial_samples,1);
AOM_Trace(1:initial_samples/2) = 1;
AOM_Trace(initial_samples/2+1:end) = -1;
r = randperm(initial_samples);
AOM_Trace = AOM_Trace(r);

AOM_Trace_Long = zeros(samples,1);
AOM_Trace_Long(1:samples_per_increment) = AOM_Trace(1);
for i=1:initial_samples
    AOM_Trace_Long(i*samples_per_increment:(i+1)*samples_per_increment) = AOM_Trace(i);
end

figure
plot(AOM_Trace_Long)

% timelength = 1e-6; %in microseconds
% minimumstep = 0.01e-6; %in microseconds (never less than 0.02 = 20 ns)
% samplingrate = 300e6; %samples per microsecond
% 
% totalsteps = floor(timelength/minimumstep);
% 
% t = transpose(0:2*pi/totalsteps:2*pi-2*pi/totalsteps);
% trace = square(t);
% r = randperm(length(trace));
% rtrace = trace(r);
% rtrace(rtrace==-1)=0;
% 
% AOM_Trace = zeros(floor(timelength*samplingrate),1);
% for i=1:length(rtrace)
%     b=i*floor(samplingrate*minimumstep)-floor(samplingrate*minimumstep)+1;
%     f=i*floor(samplingrate*minimumstep);
%     AOM_Trace(b:f)=rtrace(i);
% end
% 
% figure
% plot(AOM_Trace)