from kfp import dsl
from kfp import onprem
import kfp


@dsl.pipeline(name='pvc-test', description='is it displayed?')
def pvc_pipe():
    data_0 = dsl.ContainerOp(
        name="pvc",
        image="stellapark401/caltech101:pvc",
    ).set_display_name('logging')\
    .apply(onprem.mount_pvc("data-pvc", volume_name="stella-test-pv", volume_mount_path="/app/data"))
    
    
kfp.compiler.Compiler().compile(pvc_pipe, 'mnt_app_data.yaml')