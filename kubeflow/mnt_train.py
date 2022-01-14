from kfp import dsl
from kfp import onprem
import kfp


@dsl.pipeline(name='mnt_train', description='no use')
def pvc_pipe():
    data_0 = dsl.ContainerOp(
        name="pvc",
        image="stellapark401/caltech101:train",
    ).set_display_name('train_wh_PV')\
    .apply(onprem.mount_pvc("data-pvc", volume_name="stella-test-pv", volume_mount_path="/app/data"))
#     .apply(onprem.mount_pvc("data-pvc", volume_name="stella-test-pv", volume_mount_path="/app"))
#     얘는 exit code 2로 종료, 왜 그런지는 나중에 알아보쟈..... 쿠버네티스 짜즈..........ㅇ.....ㄴ...ㅏ
    
kfp.compiler.Compiler().compile(pvc_pipe, 'mnt_train.yaml')