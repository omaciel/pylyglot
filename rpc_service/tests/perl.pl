use Frontier::Client;

$server_url = 'http://localhost:8000/rpc_service/';
$server = Frontier::Client->new(url => $server_url);

$translation = $server->call('get_translation', 'master', 'help');
$status = $server->call('get_status');
@languages = $server->call('get_languages');

print $languages[0][0]->{'short_name'} . "\n";
print $status->{'total_packages'};
print $translation->{'help'}[0]->{'translation'} . "\n";
