import json
import io


def util_load_json(path):
    with io.open(path, mode='r', encoding='utf-8') as f:
        return json.loads(f.read())


def test_get_task_monitor_results_command(requests_mock):
    from Resec import Client, get_task_monitor_results_command

    mock_response = util_load_json('test_data/get_task_monitor_results.json')
    requests_mock.get('https://test.com/api/monitor/task-results-by-module?id=1'
                      + '&module_name=data_breaches&page=1&per-page=1000',
                      headers={'X-Pagination-Page-Count': '1'},
                      json=mock_response)

    client = Client(
        base_url='https://test.com/api/',
        verify=False,
        auth=('some_api_key', ''),
    )

    args = {
        'monitor_task_id': 1
    }

    command_function = get_task_monitor_results_command('data_breaches')
    response = command_function(client, args)

    assert response.outputs == mock_response
    assert response.outputs_prefix == 'Resec.DataBreach'
    assert response.outputs_key_field == 'id'
