from __future__ import division
import peyote
import corner

peyote.utils.setup_logger()

outdir = 'outdir'
label = 'GW150914'
time_of_event = 1126259462.422

H1, sampling_frequency, time_duration = peyote.detector.get_inteferometer('H1', epoch=time_of_event, version=1)
L1, sampling_frequency, time_duration = peyote.detector.get_inteferometer('L1', epoch=time_of_event, version=1)
IFOs = [H1, L1]

maximum_posterior_estimates = dict(
    spin11=0, spin12=0, spin13=0, spin21=0, spin22=0, spin23=0,
    luminosity_distance=410., iota=2.97305, phase=1.145,
    waveform_approximant='IMRPhenomPv2', reference_frequency=50., ra=1.375,
    dec=-1.2108, geocent_time=time_of_event, psi=2.659, mass_1=36, mass_2=29)

# Define the prior
prior = peyote.prior.parse_floats_to_fixed_priors(maximum_posterior_estimates)
prior['ra'] = peyote.prior.create_default_prior(name='ra')
prior['phase'] = peyote.prior.create_default_prior(name='phase')
prior['dec'] = peyote.prior.create_default_prior(name='dec')
prior['iota'] = peyote.prior.create_default_prior(name='iota')
prior['mass_2'] = peyote.prior.create_default_prior(name='mass_2')
prior['geocent_time'] = peyote.prior.Uniform(
    time_of_event-2, time_of_event+2, name='geocent_time')
prior['luminosity_distance'] = peyote.prior.create_default_prior(
    name='luminosity_distance')

# Create the waveformgenerator
waveformgenerator = peyote.waveform_generator.WaveformGenerator(
     peyote.source.lal_binary_black_hole, sampling_frequency,
     time_duration, parameters=prior)

# Define a likelihood
likelihood = peyote.likelihood.Likelihood(IFOs, waveformgenerator)

# Run the sampler
result = peyote.sampler.run_sampler(
    likelihood, prior, sampler='pymultinest', n_live_points=300, verbose=True,
    resume=False, outdir=outdir, use_ratio=True)

truths = [maximum_posterior_estimates[x] for x in result.search_parameter_keys]
fig = corner.corner(result.samples, labels=result.search_parameter_keys,
                    truths=truths)
fig.savefig('{}/corner.png'.format(outdir))
import IPython; IPython.embed()
