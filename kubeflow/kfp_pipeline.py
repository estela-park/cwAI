import kfp
import kfp.components as comp
from kfp import dsl

@dsl.pipeline(name='trial')
def pipe_ver0():
    ct = dsl.ContainerOp(name='stand alone', image='stellapark401/kfp:trial1').set_display_name('trial')
    
if __name__ == '__main__':
    host = 'http://192.168.1.161:30356/kubeflow'
    # host = 'http://localhost:3000'
    namespace = 'stella401'
    
    pipeline_name = 'first_try'
    pipeline_package_path = './pipeline.yaml'
    experiment_name ='first_try'
    run_name = 'first_try'
    
    client = kfp.Client(host=host, namespace=namespace)
    kfp.compiler.Compiler().compile(pipe_ver0, pipeline_package_path)
    
    # pipeline 있을 때 사용
    # pipeline_id = client.get_pipeline_id(pipeline_name)
    
    client.upload_pipeline(pipeline_package_path, pipeline_name=pipeline_name)
    
    experiment = client.create_experiment(name=experiment_name, namespace=namespace)
    run = client.run_pipeline(experiment.id, run_name, pipeline_package_path)